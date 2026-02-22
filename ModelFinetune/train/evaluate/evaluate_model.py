import os
import sys
import gc
import re  # 新增正则库
import torch
import jieba
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import evaluate
from datasets import load_dataset
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template

# ================= 1. 环境配置 =================
os.environ['UNSLOTH_USE_MODELSCOPE'] = '1'
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['HF_HUB_OFFLINE'] = '0'
os.environ['TRANSFORMERS_OFFLINE'] = '0'

# ================= 2. 配置区域 =================
# 路径配置
BASE_MODEL = "/mnt/d/workspace/PartLawyer/ModelFinetune/model" 
FINETUNED_MODEL = "/mnt/d/workspace/PartLawyer/ModelFinetune/train/outputs4/lora_model"
DATA_PATH = "/mnt/d/workspace/PartLawyer/ModelFinetune/dataset/labor_train_dataset.jsonl"
OUTPUT_DIR = "evaluation_report_v2" # 改个名，防止覆盖
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 评估参数
TEST_SAMPLE_SIZE = 30       # 建议保持 30-50
MAX_SEQ_LENGTH = 4096       # 增大上下文长度以容纳思考过程
MAX_NEW_TOKENS = 4096       # 【重要】增大生成长度，防止思考被截断
SEED = 42                   

# 系统提示词
SYSTEM_PROMPT = "你是人工智能律师阿律，精通《中华人民共和国劳动合同法》及劳动仲裁实务。请根据以下案情事实提供专业的法律建议、案件分析或文书草案。"

# ================= 3. 核心工具函数 =================

def clean_model_output(text):
    """
    【核心改进】清洗 DeepSeek 的思考过程标签
    只保留 <think>...</think> 之后的内容
    """
    # 移除 <think>...</think> 及其内部所有内容
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    # 移除可能残留的 <|im_end|> 等特殊 token
    cleaned_text = cleaned_text.replace('<|im_end|>', '').strip()
    
    return cleaned_text

def extract_keywords(text, top_k=5):
    import jieba.analyse
    # 只有当文本够长时才提取，防止报错
    if len(text) < 5: return []
    return jieba.analyse.extract_tags(text, topK=top_k)

def calculate_keyword_recall(pred_text, ref_text):
    ref_keywords = set(extract_keywords(ref_text, top_k=10))
    if not ref_keywords:
        return 0.0
    
    pred_words = set(jieba.cut(pred_text))
    matched = ref_keywords.intersection(pred_words)
    return len(matched) / len(ref_keywords)

def get_dataset(data_path, sample_size, seed):
    print(f"📋 正在加载数据集: {data_path}")
    dataset = load_dataset("json", data_files=data_path, split="train")
    dataset = dataset.shuffle(seed=seed)
    test_dataset = dataset.select(range(sample_size))
    print(f"✅ 已随机抽取 {sample_size} 条数据用于评估 (Seed={seed})")
    return test_dataset

# ================= 4. 模型评估主逻辑 =================

def run_inference_and_score(model_path, model_label, dataset, rouge_metric):
    print(f"\n🚀 正在加载模型 [{model_label}]...")
    print(f"   路径: {model_path}")

    # 强制清理显存
    gc.collect()
    torch.cuda.empty_cache()

    try:
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name = model_path,
            max_seq_length = MAX_SEQ_LENGTH,
            dtype = None,
            load_in_4bit = True,
        )
        FastLanguageModel.for_inference(model)
        
        tokenizer = get_chat_template(tokenizer, chat_template = "chatml")
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return []

    results = []
    
    print(f"⏳ 开始推理 ({len(dataset)} 条)...")
    for i, item in enumerate(tqdm(dataset, desc=f"Testing {model_label}")):
        user_content = item['instruction']
        if 'input' in item and item['input']:
            user_content += "\n" + str(item['input'])
            
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]
        
        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt = True,
            return_tensors = "pt",
        ).to("cuda")

        with torch.no_grad():
            outputs = model.generate(
                input_ids = inputs,
                max_new_tokens = MAX_NEW_TOKENS, # 【重要】增大生成上限
                temperature = 0.6,     # 【调整】稍微调高一点点，防止复读机，但保持低位
                top_p = 0.9,
                repetition_penalty = 1.1,
                pad_token_id = tokenizer.eos_token_id
            )
            
        generated_ids = outputs[0][len(inputs[0]):]
        raw_prediction = tokenizer.decode(generated_ids, skip_special_tokens=False).strip() # 先保留特殊token以便调试
        
        # 【重要】清洗思考过程，只评估正文
        clean_prediction = clean_model_output(raw_prediction)
        
        reference = item['output']

        # --- 计算指标 ---
        
        # 1. ROUGE (字面重叠)
        pred_tokens = " ".join(jieba.cut(clean_prediction))
        ref_tokens = " ".join(jieba.cut(reference))
        
        # 防止空字符串报错
        if not pred_tokens.strip(): pred_tokens = "空"
        
        rouge_scores = rouge_metric.compute(predictions=[pred_tokens], references=[ref_tokens])
        
        # 2. Keyword Recall (核心词命中率)
        kw_recall = calculate_keyword_recall(clean_prediction, reference)

        results.append({
            "id": i,
            "model": model_label,
            "instruction": user_content,
            "reference": reference,
            "raw_prediction": raw_prediction, # 保留原始输出用于Debug（看思考过程）
            "prediction": clean_prediction,   # 清洗后用于评分的输出
            "rouge-1": rouge_scores['rouge1'],
            "rouge-l": rouge_scores['rougeL'],
            "keyword_recall": kw_recall,
            "char_len": len(clean_prediction)
        })

    # 彻底清理显存
    del model, tokenizer
    gc.collect()
    torch.cuda.empty_cache()
    
    return results

# ================= 5. 主程序 =================
if __name__ == "__main__":
    # 1. 准备数据
    test_data = get_dataset(DATA_PATH, TEST_SAMPLE_SIZE, SEED)
    rouge = evaluate.load("rouge")

    # 2. 评估 Base Model
    base_results = run_inference_and_score(BASE_MODEL, "Base Model", test_data, rouge)
    
    # 3. 评估 Finetuned Model
    fine_results = run_inference_and_score(FINETUNED_MODEL, "Finetuned Model", test_data, rouge)

    # 4. 合并数据与分析
    if base_results and fine_results:
        df_base = pd.DataFrame(base_results)
        df_fine = pd.DataFrame(fine_results)
        df_all = pd.concat([df_base, df_fine])

        # 保存详细对比表 (CSV)
        df_wide = df_base[['id', 'instruction', 'reference', 'prediction', 'rouge-l', 'keyword_recall']].copy()
        df_wide.columns = ['id', 'instruction', 'reference', 'Base_Pred', 'Base_RougeL', 'Base_KW']
        
        df_fine_sub = df_fine[['id', 'prediction', 'rouge-l', 'keyword_recall']].copy()
        df_fine_sub.columns = ['id', 'Fine_Pred', 'Fine_RougeL', 'Fine_KW']
        
        df_comparison = pd.merge(df_wide, df_fine_sub, on='id')
        
        # 计算提升率
        df_comparison['RougeL_Improv'] = df_comparison['Fine_RougeL'] - df_comparison['Base_RougeL']
        df_comparison['KW_Improv'] = df_comparison['Fine_KW'] - df_comparison['Base_KW']
        
        detailed_csv_path = os.path.join(OUTPUT_DIR, "detailed_comparison.csv")
        df_comparison.to_csv(detailed_csv_path, index=False, encoding='utf-8-sig')

        # --- 绘图 ---
        plt.figure(figsize=(18, 10))
        sns.set_theme(style="whitegrid")

        # 图1: ROUGE-L 均值对比
        plt.subplot(2, 2, 1)
        sns.barplot(data=df_all, x='model', y='rouge-l', palette="viridis")
        plt.title('ROUGE-L Score (Content Similarity)', fontsize=14)
        
        # 图2: 关键词召回率对比
        plt.subplot(2, 2, 2)
        sns.barplot(data=df_all, x='model', y='keyword_recall', palette="magma")
        plt.title('Legal Keyword Recall', fontsize=14)
        
        # 图3: 答案长度分布 (检查是否过短或过长)
        plt.subplot(2, 2, 3)
        sns.histplot(data=df_all, x='char_len', hue='model', kde=True, element="step")
        plt.title('Answer Length Distribution (Cleaned)', fontsize=14)

        # 图4: 散点图
        plt.subplot(2, 2, 4)
        sns.scatterplot(data=df_all, x='rouge-l', y='keyword_recall', hue='model', alpha=0.7, s=100)
        plt.title('Quality Trade-off', fontsize=14)

        plt.tight_layout()
        chart_path = os.path.join(OUTPUT_DIR, "evaluation_dashboard.png")
        plt.savefig(chart_path)
        
        print("\n" + "="*50)
        print("✅ 评估完成！请查看 output 目录")
        print(f"📊 可视化报告: {chart_path}")
        print(f"📑 详细对比表: {detailed_csv_path}")
        print(f"📈 Base 平均 ROUGE-L: {df_base['rouge-l'].mean():.4f}")
        print(f"📈 Fine 平均 ROUGE-L: {df_fine['rouge-l'].mean():.4f}")
        print("="*50)