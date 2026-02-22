import os
# 依然保持离线模式（可选）
os.environ["TRANSFORMERS_OFFLINE"] = "1"

from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template

# 1. 配置路径
# model_name 指向你保存的 LoRA 文件夹
model_name = "outputs4/lora_model" 
max_seq_length = 2048
load_in_4bit = True

# 2. 加载模型和 Tokenizer
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = model_name,
    max_seq_length = max_seq_length,
    dtype = None,
    load_in_4bit = load_in_4bit,
)

# 3. 切换到推理模式（这会让模型运行速度提升 2 倍）
FastLanguageModel.for_inference(model)

# 4. 配置 ChatML 模板 (必须与训练时一致)
tokenizer = get_chat_template(
    tokenizer,
    chat_template = "chatml",
    mapping = {"role" : "role", "content" : "content", "user" : "user", "assistant" : "assistant"},
)

# 5. 准备对话
# 这里的 SYSTEM_PROMPT 建议与训练时完全一致，以获得最佳效果
SYSTEM_PROMPT = "你是人工智能律师阿律，精通《中华人民共和国劳动法》及劳动仲裁实务。请根据以下案情事实提供专业的法律建议、案件分析或文书草案。"

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "帮我写一份劳动仲裁申请书的模板"},
]

# 6. 转化为模型输入的格式
inputs = tokenizer.apply_chat_template(
    messages,
    tokenize = True,
    add_generation_prompt = True, # 关键：添加这一行以诱导模型开始回复
    return_tensors = "pt",
).to("cuda")

# 7. 生成回复
print("阿律正在思考...\n")
outputs = model.generate(
    input_ids = inputs,
    max_new_tokens = 1024, # 允许生成的最大长度
    use_cache = True,
    temperature = 0.7,     # 采样温度，法律建议可以设低一点增加稳定性
    top_p = 0.9,
)

# 8. 解码并打印结果
response = tokenizer.batch_decode(outputs)
# 提取助手回复的部分（过滤掉 Prompt）
print(response[0].split("<|im_start|>assistant")[-1].replace("<|im_end|>", "").strip())