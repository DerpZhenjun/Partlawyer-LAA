import os
import tempfile
import re 
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi.background import BackgroundTasks
from typing import Dict, Any

from WenShu.WIAdocx import generate_WIAdocx

router = APIRouter()

def remove_file(path: str):
    try:
        os.remove(path)
    except Exception:
        pass

# --- 2. 添加转换函数 ---
def camel_to_snake(name):
    """把驼峰命名 (hiredateYear) 转为 下划线命名 (hiredate_year)"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

@router.post("/generate")
async def generate_wia(req: Dict[str, Any], background_tasks: BackgroundTasks):
    try:
        # --- 3. 数据处理核心逻辑 ---
        cleaned_data = {}
        for key, value in req.items():
            # 去除字符串两端空格
            val = value.strip() if isinstance(value, str) else value
            
            # 关键步骤：把 key 转成下划线格式
            # 例如：前端传 'hiredateYear' -> 这里变成 'hiredate_year'
            new_key = camel_to_snake(key)
            
            cleaned_data[new_key] = val
            
            # 为了保险，把原始 key 也存一份
            cleaned_data[key] = val

        # 打印一下数据，看看 key 对不对 (调试用，上线可删)
        print("最终用于生成的数据 keys:", list(cleaned_data.keys()))

        doc = generate_WIAdocx(cleaned_data)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            doc.save(tmp.name)
            tmp_path = tmp.name

        background_tasks.add_task(remove_file, tmp_path)

        # 获取文件名 (尝试多种可能的 key)
        name = cleaned_data.get('claimant_name') or cleaned_data.get('claimantName') or "申请人"
        filename = f"{name}的工伤仲裁申请书.docx"

        return FileResponse(
            tmp_path,
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))