# $env:HF_ENDPOINT = "https://hf-mirror.com"
import os
from huggingface_hub import snapshot_download

# 配置路径
CONFIG = {
    "ShengbinYue/DISC-Law-SFT": r"D:\workspace\PartLawyer\ModelFinetune\dataset\DISC-Law-SFT",
    "Skepsun/lawyer_llama_data": r"D:\workspace\PartLawyer\ModelFinetune\dataset\lawyer_llama_data"
}

def download_raw_datasets():
    print("🚀 开始原样下载任务 (镜像加速已开启)...")
    
    # 在代码中也可以再次强制设置环境变量，确保生效
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

    for hf_repo, local_dir in CONFIG.items():
        print(f"\n------------------------------------------------")
        print(f"📦 正在处理: {hf_repo}")
        print(f"📂 目标路径: {local_dir}")
        
        try:
            # 1. 确保目录存在
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)

            # 2. 使用 snapshot_download 下载原始文件
            # repo_type="dataset" 非常重要，否则默认会去找模型
            # local_dir_use_symlinks=False 确保下载的是真实文件而不是快捷方式
            snapshot_download(
                repo_id=hf_repo,
                repo_type="dataset", 
                local_dir=local_dir,
                local_dir_use_symlinks=False,
                resume_download=True,
                # 如果你想过滤掉 .git 文件夹等杂项，可以取消下面注释，
                # 但既然要是“原封不动”，建议不加过滤
                # ignore_patterns=[".gitattributes", "README.md"] 
            )
            
            print(f"   ✅ 下载成功！原始文件已保存在: {local_dir}")
            
        except Exception as e:
            print(f"   ❌ 下载失败 {hf_repo}: {e}")

if __name__ == "__main__":
    download_raw_datasets()
    print("\n✨ 所有下载任务结束。")