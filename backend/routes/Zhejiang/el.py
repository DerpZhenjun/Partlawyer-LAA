import os
import tempfile
import traceback
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi.background import BackgroundTasks
from pydantic import BaseModel
from typing import List

# 引入生成逻辑
from WenShu.Zhejiang.ELdocx import generate_ELdocx

router = APIRouter()

# --- 数据模型 ---
class EvidenceItem(BaseModel):
    id: int
    name: str = ""      
    source: str = ""    
    object: str = ""    # 兼容前端字段

class EvidenceRequest(BaseModel):
    evidence_list: List[EvidenceItem]

def remove_file(path: str):
    try:
        os.remove(path)
    except Exception:
        pass

@router.post("/generate")
async def generate_zj_el(req: EvidenceRequest, background_tasks: BackgroundTasks):
    try:
        # 1. 准备数据：统一打包成一个列表，不拆分首行
        # 构建 3 个平行列表 + 1 个字典列表 (为了最大兼容性)
        list_names = []
        list_sources = []
        list_objects = []
        list_dicts = [] # 包含完整信息的字典列表

        for item in req.evidence_list:
            n_str = str(item.name if item.name else "")
            s_str = str(item.source if item.source else "")
            o_str = str(item.object if item.object else "")

            list_names.append(n_str)
            list_sources.append(s_str)
            list_objects.append(o_str)
            
            # 字典用于逻辑层遍历
            list_dicts.append({
                'evidence_name': n_str,
                'evidence_source': s_str,
                'evidence_object': o_str
            })

        # 2. 定位模板
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backend_root = os.path.dirname(os.path.dirname(current_dir))
        
        template_path = os.path.join(
            backend_root, 
            'templates_docx',  
            'Zhejiang', 
            '证据清单.docx'
        )

        if not os.path.exists(template_path):
            fallback = r"D:\workspace\PartLawyer\backend\templates_docx\Zhejiang\证据清单.docx"
            if os.path.exists(fallback):
                template_path = fallback
            else:
                raise HTTPException(status_code=500, detail=f"模板未找到: {template_path}")

        # 3. 调用生成函数 (改为 5 参数模式，与广东版保持一致)
        # 即使浙江版不需要某些列表，传进去也没坏处，保持接口统一最好维护
        print(f"调用浙江生成函数，数据条数: {len(list_dicts)}")
        
        doc = generate_ELdocx(
            list_names,     # names
            list_sources,   # sources
            list_objects,   # objects
            list_dicts,     # dicts (核心数据源)
            template_path   # path
        )

        # 4. 保存返回
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            doc.save(tmp.name)
            tmp_path = tmp.name

        background_tasks.add_task(remove_file, tmp_path)
        
        return FileResponse(
            tmp_path, 
            filename='浙江证据清单.docx',
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        print(f"Error generating ZJ EL:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))