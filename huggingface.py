from huggingface_hub import HfApi

api = HfApi()

# --- 配置信息 ---
token = "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"  # 建议使用新生成的Token
repo_id = "DerpZhenjun/PartLawyer-LAA"

# 本地文件夹的具体路径
path_hubert = r"D:\workspace\PartLawyer\GPT-SoVITS\GPT_SoVITS\pretrained_models\chinese-hubert-base"
path_roberta = r"D:\workspace\PartLawyer\GPT-SoVITS\GPT_SoVITS\pretrained_models\chinese-roberta-wwm-ext-large"

print("🚀 开始上传预训练模型组件...")

# 1. 上传 chinese-hubert-base
print(f"正在上传: chinese-hubert-base...")
api.upload_folder(
    folder_path=path_hubert,
    path_in_repo="pretrained_models/chinese-hubert-base", # 这样会创建预训练模型层级文件夹
    repo_id=repo_id,
    repo_type="model",
    token=token
)

# 2. 上传 chinese-roberta-wwm-ext-large
print(f"正在上传: chinese-roberta-wwm-ext-large...")
api.upload_folder(
    folder_path=path_roberta,
    path_in_repo="pretrained_models/chinese-roberta-wwm-ext-large",
    repo_id=repo_id,
    repo_type="model",
    token=token
)

print(f"✅ 所有组件上传成功！")
print(f"预览地址: https://huggingface.co/{repo_id}/tree/main/pretrained_models")