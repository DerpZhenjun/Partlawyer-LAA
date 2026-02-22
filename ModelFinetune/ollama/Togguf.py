from unsloth import FastLanguageModel

# 配置路径
lora_path = "/mnt/d/workspace/PartLawyer/ModelFinetune/train/outputs/lora_model"

# 1. 加载模型
# 【关键修改】：load_in_4bit 必须设为 False
# 只有这样，LoRA 权重才会合并到 16bit 的原始权重中，避免量化误差导致的胡言乱语
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = lora_path,
    max_seq_length = 2048,
    dtype = None,           # 保持 None，Unsloth 会根据硬件自动选择 float16 或 bfloat16
    load_in_4bit = False,   # 转换为 GGUF 时请务必关闭 4bit 加载
    local_files_only = True,
)

# 2. 导出为 GGUF
print("开始转换 GGUF (正在进行 16bit 合并)...")

# 提示：由于此时是 16bit 加载，合并过程会占用约 14-16GB 的内存（RAM）
# 如果你的显存不足，Unsloth 会自动切换到系统内存处理。
model.save_pretrained_gguf(
    "outputs/gguf_output", 
    tokenizer, 
    quantization_method = "q4_k_m"  # 如果对精度要求极高，也可以尝试 "q8_0"
)

print("转换完成！请重新在 Ollama 中运行 create 命令。")