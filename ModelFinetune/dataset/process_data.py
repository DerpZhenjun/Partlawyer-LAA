import json
import os
import glob
from tqdm import tqdm

# ================= 配置区域 =================
BASE_DIR = r"D:\workspace\PartLawyer\ModelFinetune\dataset"
DISC_DIR = os.path.join(BASE_DIR, "DISC-Law-SFT")
LAWYER_DIR = os.path.join(BASE_DIR, "lawyer_llama_data")
OUTPUT_FILE = os.path.join(BASE_DIR, "labor_train_dataset.jsonl")

# ================= 精细化筛选关键词配置 =================

# 1. 核心高权重词：只要出现，极大概率是劳动法/仲裁相关
CORE_LABOR_WORDS = [
    "劳动仲裁", "劳动争议", "欠薪", "克扣工资", "违法辞退", 
    "劳动合同法", "解除劳动关系", "劳动监察", "未签劳动合同",
    "经济补偿金", "双倍工资", "加班费", "工伤认定", "职业病诊断",
    "劳动关系认定", "非法用工", "违法解除", "仲裁委", "仲裁庭"
]

# 2. 普通相关词：需要配合上下文，命中两个以上才视为有效
NORMAL_LABOR_WORDS = [
    "工资", "薪资", "底薪", "提成", "奖金", "社保", "五险一金", 
    "公积金", "调岗", "离职", "辞职", "入职", "试用期", "转正", 
    "加班", "调休", "休假", "年假", "产假", "病假", "考勤", 
    "劳务派遣", "外包", "竞业限制", "保密协议", "辞退", "解雇",
    "人事", "HR", "报酬", "基本工资", "绩效"
]

# 3. 强力排除词：只要出现，通常属于刑事、行政或其他无关领域
# 增加“指控”、“公诉”、“有期徒刑”等词可以过滤掉你之前遇到的刑事判决数据
EXCLUDE_WORDS = [
    "检察院", "公诉", "指控", "犯罪事实", "判处有期徒刑", "拘役", "有期徒刑",
    "盗窃罪", "受贿罪", "放火罪", "失火罪", "玩忽职守罪", "强奸罪", 
    "寻衅滋事", "故意伤害", "毒品", "杀人", "抢劫", "贪污", "赃款",
    "交通肇事", "信用卡诈骗", "离婚协议", "遗产继承", "房产买卖", "缓刑",
    "剥夺政治权利", "没收财产", "刑事责任", "公诉机关"
]

# ================= 处理逻辑 =================

def is_labor_related(instruction, input_text, output):
    """
    精细化筛选逻辑：
    1. 排除包含刑事/无关领域关键词的文本
    2. 优先保留包含核心词（如“仲裁”）的文本
    3. 如果没有核心词，则要求普通词（如“工资”+“解雇”）命中至少2个不同词汇
    """
    full_text = f"{instruction} {input_text} {output}".replace("\n", " ")
    
    # --- 步骤 1: 强力排除 ---
    for word in EXCLUDE_WORDS:
        if word in full_text:
            return False
            
    # --- 步骤 2: 核心词判定 ---
    for word in CORE_LABOR_WORDS:
        if word in full_text:
            return True
            
    # --- 步骤 3: 普通词频率/密度判定 ---
    found_words = set()
    for word in NORMAL_LABOR_WORDS:
        if word in full_text:
            found_words.add(word)
            if len(found_words) >= 2: # 命中至少两个不同的普通劳动词
                return True
                
    return False

def format_example(instruction, input_text, output):
    """统一返回 Alpaca 格式"""
    return {
        "instruction": instruction.strip(),
        "input": input_text.strip() if input_text else "",
        "output": output.strip()
    }

def process_lawyer_llama():
    json_path = os.path.join(LAWYER_DIR, "all.json")
    data_list = []
    if not os.path.exists(json_path): return []

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        for item in tqdm(raw_data, desc="Processing Lawyer Llama"):
            inst = item.get('instruction', item.get('q', ''))
            inp = item.get('input', '')
            out = item.get('output', item.get('a', ''))
            if inst and out and is_labor_related(inst, inp, out):
                data_list.append(format_example(inst, inp, out))
    except Exception as e:
        print(f"❌ Lawyer Llama 处理错误: {e}")
    return data_list

def process_disc_law():
    data_list = []
    files = glob.glob(os.path.join(DISC_DIR, "*.jsonl"))
    for file_path in files:
        filename = os.path.basename(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in tqdm(f, desc=f"Processing {filename}"):
                    item = json.loads(line)
                    # 动态映射字段
                    inst = item.get('instruction', item.get('title', item.get('input', '')))
                    out = item.get('output', item.get('target', ''))
                    inp = item.get('context', '')
                    
                    if inst and out and is_labor_related(inst, inp, out):
                        data_list.append(format_example(inst, inp, out))
        except Exception as e:
            print(f"❌ 文件 {filename} 处理失败: {e}")
    return data_list

def main():
    print(f"🚀 开始精细化提取【劳动仲裁】数据...")
    
    all_data = []
    all_data.extend(process_lawyer_llama())
    all_data.extend(process_disc_law())
    
    # 去重处理（基于指令和输出的哈希）
    unique_data = []
    seen = set()
    for d in all_data:
        identifier = hash(d['instruction'] + d['output'])
        if identifier not in seen:
            unique_data.append(d)
            seen.add(identifier)

    print(f"\n📊 原始筛选: {len(all_data)} 条 -> 去重后: {len(unique_data)} 条")
    
    # 保存结果
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for entry in unique_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
    print(f"✅ 处理完成！文件已保存至: {OUTPUT_FILE}")
    print("💡 建议：训练前请随机抽取 10 条检查是否仍含有刑事案件。")

if __name__ == "__main__":
    main()