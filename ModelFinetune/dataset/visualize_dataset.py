import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import jieba
from wordcloud import WordCloud
import numpy as np  # 确保导入numpy

# ================= 配置区域 =================
DATASET_PATH = r"D:\workspace\PartLawyer\ModelFinetune\dataset\labor_train_dataset.jsonl"
# Windows系统默认黑体路径，用于显示中文
FONT_PATH = "C:/Windows/Fonts/simhei.ttf" 
OUTPUT_DIR = "paper_figures" 

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 设置绘图风格和中文字体
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

# ================= 1. 加载数据 =================
print("正在加载数据集...")
data = []
with open(DATASET_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data.append(json.loads(line))
        except:
            continue

df = pd.DataFrame(data)
print(f"数据加载完毕，共 {len(df)} 条样本")

# 计算长度
df['instruction_len'] = df['instruction'].apply(len)
df['output_len'] = df['output'].apply(len)
df['total_len'] = df['instruction_len'] + df['output_len']

# ================= 2. 绘图逻辑 =================

def plot_source_distribution():
    """图1：数据来源分布饼图"""
    if 'source' not in df.columns:
        print("⚠️ 数据中未包含 source 字段，跳过来源分布图")
        return

    plt.figure(figsize=(8, 6))
    source_counts = df['source'].value_counts()
    colors = sns.color_palette('pastel')[0:len(source_counts)]
    
    plt.pie(source_counts, labels=source_counts.index, autopct='%1.1f%%', 
            startangle=140, colors=colors, textprops={'fontsize': 12})
    plt.title('劳动法数据集来源分布', fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/1_source_distribution.png", dpi=300)
    print("✅ 已生成：数据来源分布图")

def plot_length_distribution():
    """图2：文本长度分布直方图"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # 输入长度
    sns.histplot(df['instruction_len'], bins=50, kde=True, ax=axes[0], color='skyblue')
    axes[0].set_title('输入文本长度分布', fontsize=14)
    axes[0].set_xlabel('字符数 ')
    axes[0].set_ylabel('频次')

    # 输出长度
    sns.histplot(df['output_len'], bins=50, kde=True, ax=axes[1], color='salmon')
    axes[1].set_title('输出 文本长度分布', fontsize=14)
    axes[1].set_xlabel('字符数')
    axes[1].set_ylabel('频次')

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/2_length_distribution.png", dpi=300)
    print("✅ 已生成：长度分布图")

def plot_keyword_frequency():
    """图3：Top 15 高频关键词"""
    LABOR_KEYWORDS = [
        "劳动", "工资", "辞退", "解雇", "离职", "试用期", "加班", "工伤", 
        "社保", "公积金", "年假", "补偿金", "赔偿金", "违约金", "竞业限制", 
        "欠薪", "调岗", "仲裁", "劳动争议", "合同"
    ]
    
    # 简单的文本拼接
    all_text = " ".join(df['instruction']) + " " + " ".join(df['output'])
    
    keyword_counts = {}
    for kw in LABOR_KEYWORDS:
        keyword_counts[kw] = all_text.count(kw)
    
    # 转为 DataFrame 方便绘图
    kw_df = pd.DataFrame(list(keyword_counts.items()), columns=['Keyword', 'Count'])
    kw_df = kw_df.sort_values(by='Count', ascending=False).head(15)

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Count', y='Keyword', data=kw_df, hue='Keyword', palette='viridis', legend=False)
    plt.title('劳动法相关高频关键词 Top 15', fontsize=14)
    plt.xlabel('出现频次')
    plt.ylabel('关键词')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/3_keyword_frequency.png", dpi=300)
    print("✅ 已生成：关键词频率图")

def generate_wordcloud():
    """图4：生成词云"""
    # 提取部分文本用于生成词云（避免内存溢出）
    sample_text = " ".join(df['instruction'].sample(frac=0.5, random_state=42)) + \
                  " ".join(df['output'].sample(frac=0.5, random_state=42))
    
    # 结巴分词
    print("正在进行分词（可能需要几秒钟）...")
    words = jieba.lcut(sample_text)
    
    # 过滤停用词和单字
    stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '如何', '什么', '怎么', '咨询', '问题', '请问', '那个', '这个'}
    filtered_words = [word for word in words if len(word) > 1 and word not in stopwords]
    
    text_clean = " ".join(filtered_words)

    wc = WordCloud(
        font_path=FONT_PATH,
        background_color='white',
        width=1000,
        height=600,
        max_words=200,
        colormap='magma'
    ).generate(text_clean)

    plt.figure(figsize=(10, 6))
    
    # 🔥🔥🔥 核心修改：使用 .to_image() 绕过 numpy 2.0 的兼容性问题
    plt.imshow(wc.to_image(), interpolation='bilinear')
    
    plt.axis('off')
    plt.title('劳动法数据集核心词云', fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/4_wordcloud.png", dpi=300)
    print("✅ 已生成：词云图")

def plot_instruction_vs_output():
    """图5：输入长度 vs 输出长度 散点密度图"""
    plt.figure(figsize=(8, 6))
    plt.hexbin(df['instruction_len'], df['output_len'], gridsize=40, cmap='Blues', mincnt=1)
    cb = plt.colorbar(label='样本数量')
    plt.xlabel('输入 (Instruction) 长度')
    plt.ylabel('输出 (Output) 长度')
    plt.title('输入长度 vs 输出长度 分布密度', fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/5_scatter_density.png", dpi=300)
    print("✅ 已生成：输入输出长度相关图")

# ================= 3. 执行 =================
if __name__ == "__main__":
    plot_source_distribution()   # 如果没有 source 字段，此图会跳过
    plot_length_distribution()   # 论文核心：展示数据长度分布
    plot_keyword_frequency()     # 论文核心：展示数据相关性
    plot_instruction_vs_output() # 论文补充：展示数据复杂度
    generate_wordcloud()         # 论文展示：视觉效果好
    
    print(f"\n🎉 所有图表已保存在 {OUTPUT_DIR} 文件夹下。")