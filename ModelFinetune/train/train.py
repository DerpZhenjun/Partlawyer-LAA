import os
import sys
import matplotlib

# --- 1. 环境配置 ---
# 强制 matplotlib 使用非交互后端，防止无头服务器报错
matplotlib.use('Agg') 
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import torch
import matplotlib.pyplot as plt
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments, EarlyStoppingCallback
from unsloth import is_bfloat16_supported

# --- 2. 参数配置 ---
model_name = "/mnt/d/workspace/PartLawyer/ModelFinetune/model"
dataset_path = "/mnt/d/workspace/PartLawyer/ModelFinetune/dataset/labor_train_dataset.jsonl"
output_dir = "outputs"
max_seq_length = 2048
load_in_4bit = True 

# --- 3. 加载模型 ---
print(f"Loading model from: {model_name}")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = model_name,
    max_seq_length = max_seq_length,
    dtype = None,
    load_in_4bit = load_in_4bit,
    local_files_only = True,
)

# 3.1 防御性代码：确保 Pad Token 存在
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# --- 4. 配置 LoRA ---
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
    use_gradient_checkpointing = "unsloth", # Unsloth 特有优化
    random_state = 3407,
    use_rslora = False,
    loftq_config = None,
)

# --- 5. 数据处理 (ChatML) ---
# 设置 ChatML 模板
tokenizer = get_chat_template(
    tokenizer,
    chat_template = "chatml",
    mapping = {"role" : "role", "content" : "content", "user" : "user", "assistant" : "assistant"},
)

SYSTEM_PROMPT = "你是人工智能律师阿律，精通《中华人民共和国劳动法》及劳动仲裁实务。请根据以下案情事实提供专业的法律建议、案件分析或文书草案。"

def formatting_prompts_func(examples):
    instructions = examples["instruction"]
    inputs       = examples["input"]
    outputs      = examples["output"]
    texts = []
    
    for instruction, input, output in zip(instructions, inputs, outputs):
        user_content = instruction
        if input and len(str(input)) > 0:
            user_content += "\n" + str(input)
            
        conversation = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": output},
        ]
        
        # 生成不带 Token 的纯文本
        text = tokenizer.apply_chat_template(
            conversation, 
            tokenize = False, 
            add_generation_prompt = False
        )
        
        # 手动添加 EOS Token
        text += tokenizer.eos_token
        
        texts.append(text)
        
    return { "text" : texts }

print("正在加载和处理数据...")
dataset = load_dataset("json", data_files={"train": dataset_path}, split="train")

# 打印一条数据检查格式是否正确 (Debug 用)
print(">>> 原始数据示例:", dataset[0])

# 这里的 seed 建议固定，保证每次切分的数据集一致
dataset = dataset.train_test_split(test_size=0.1, seed=42)

# num_proc=1 防止多进程导致 Tokenizer 序列化失败报错
train_dataset = dataset["train"].map(formatting_prompts_func, batched = True, num_proc=1)
eval_dataset = dataset["test"].map(formatting_prompts_func, batched = True, num_proc=1)

# 打印处理后的数据示例
# 注意：如果日志中看到两个 <|im_end|> 是正常的，这好过没有 EOS
print(">>> 处理后数据示例 (最后50字符):", train_dataset[0]["text"][-50:])

# --- 6. 训练参数 ---
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = train_dataset,
    eval_dataset = eval_dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 1, 
    packing = False,      
    args = TrainingArguments(
        per_device_train_batch_size = 1,
        gradient_accumulation_steps = 8, 
        per_device_eval_batch_size = 1,
        eval_accumulation_steps = 1,
        warmup_steps = 10,
        num_train_epochs = 5,
        learning_rate = 2e-4,
        fp16 = not is_bfloat16_supported(),
        bf16 = is_bfloat16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = output_dir,
        report_to = "none",
        
        # 【👇 核心修复点 👇】
        # 将 evaluation_strategy 改为 eval_strategy
        eval_strategy = "steps", 
        
        eval_steps = 40,
        save_steps = 40,
        load_best_model_at_end = True,
        save_total_limit = 2,
        metric_for_best_model = "loss",
        greater_is_better = False,
        gradient_checkpointing = True, 
    ),
    callbacks = [EarlyStoppingCallback(early_stopping_patience = 3)],
)

# --- 7. 训练与保存 ---
print("开始训练...")
trainer_stats = trainer.train()

print(f"正在保存 LoRA 适配器至: {output_dir}/lora_model")
model.save_pretrained(f"{output_dir}/lora_model")
tokenizer.save_pretrained(f"{output_dir}/lora_model")

# --- 8. 绘图 ---
print("正在绘制 Loss 曲线...")
history = trainer.state.log_history

train_losses = []
train_steps = []
eval_losses = []
eval_steps = []

for entry in history:
    if 'loss' in entry:
        train_losses.append(entry['loss'])
        train_steps.append(entry['step'])
    if 'eval_loss' in entry:
        eval_losses.append(entry['eval_loss'])
        eval_steps.append(entry['step'])

if len(train_losses) > 0:
    plt.figure(figsize=(10, 6))
    plt.plot(train_steps, train_losses, label='Train Loss', alpha=0.6)
    
    if len(eval_losses) > 0:
        plt.plot(eval_steps, eval_losses, label='Eval Loss', marker='o', linestyle='--', color='red')
    
    plt.xlabel('Steps')
    plt.ylabel('Loss')
    plt.title(f'Training Loss Curve (Final Train Loss: {train_losses[-1]:.4f})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    save_path = os.path.join(output_dir, "loss_curve.png")
    plt.savefig(save_path)
    print(f"曲线图已保存至 {save_path}")
else:
    print("未找到 Loss 数据，跳过绘图。")

print("训练结束！请进行下一步：GGUF 转换。")