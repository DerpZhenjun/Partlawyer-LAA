import os
import logging
import tempfile
from pathlib import Path
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# 引入业务逻辑模块
from WenShu.Guangdong.ELdocx import generate_ELdocx

# 配置日志记录器
logger = logging.getLogger(__name__)

router = APIRouter()

# --- 数据传输对象 (DTO) ---

class EvidenceItem(BaseModel):
    id: int = Field(..., description="证据ID")
    name: str = Field(default="", description="证据名称")
    content: str = Field(default="", description="证明内容/证据详情")

class EvidenceRequest(BaseModel):
    evidence_list: List[EvidenceItem]

# --- 辅助函数 ---

def cleanup_temp_file(path: str):
    """后台任务：清理临时生成的文件的"""
    try:
        path_obj = Path(path)
        if path_obj.exists():
            path_obj.unlink()
            logger.debug(f"Temporary file removed: {path}")
    except Exception as e:
        logger.warning(f"Failed to remove temporary file {path}: {e}")

# --- API 路由 ---

@router.post("/generate", summary="生成广东省证据清单文档")
async def generate_gd_evidence(req: EvidenceRequest, background_tasks: BackgroundTasks):
    """
    接收证据列表数据，基于 Word 模板生成《证据清单》文档。
    """
    try:
        # 1. 数据预处理：构建生成引擎所需的特定数据结构
        # 注意：下游函数 generate_ELdocx 需要拆分的列表数据以及冗余的字典映射
        evidence_names: List[str] = []
        evidence_contents: List[str] = []
        evidence_details: List[Dict[str, str]] = []

        for item in req.evidence_list:
            # 确保数据为字符串类型，处理 None 值
            name_str = str(item.name or "")
            content_str = str(item.content or "")

            evidence_names.append(name_str)
            evidence_contents.append(content_str)

            # 构建详细映射，包含遗留系统所需的字段别名 (alias)
            evidence_details.append({
                'name': name_str,
                'content': content_str,
                # 兼容性字段映射，确保模板引擎能正确识别
                'evidence_name': name_str,
                'testify_content': content_str
            })

        # 2. 解析模板路径
        # 使用 pathlib 处理路径，向上回溯至 backend 根目录
        base_dir = Path(__file__).resolve().parent.parent.parent
        template_path = base_dir / "templates_docx" / "Guangdong" / "证据清单.docx"

        if not template_path.exists():
            logger.error(f"Template file missing at: {template_path}")
            raise FileNotFoundError(f"证据清单模板文件未找到")

        # 3. 调用核心生成逻辑
        logger.info(f"Invoking generate_ELdocx with {len(evidence_names)} items.")
        
        doc = generate_ELdocx(
            evidence_names,      # 证据名称列表
            evidence_contents,   # 证明内容列表
            evidence_details,    # 详细结构化数据
            str(template_path)   # 模板绝对路径
        )

        # 4. 处理文件输出
        # 创建命名临时文件，确保文件关闭后不会立即被系统删除，交由 BackgroundTasks 处理
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
            doc.save(tmp_file.name)
            tmp_path = tmp_file.name

        # 注册后台清理任务
        background_tasks.add_task(cleanup_temp_file, tmp_path)

        logger.info(f"Document generated successfully: {tmp_path}")
        
        return FileResponse(
            tmp_path,
            filename='证据清单.docx',
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # 记录完整堆栈信息以便排查，向前端返回通用错误信息
        logger.exception("Error occurred during evidence list generation.")
        raise HTTPException(status_code=500, detail=f"生成文档失败: {str(e)}")