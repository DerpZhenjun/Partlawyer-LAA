from __future__ import annotations

import os
import tempfile

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator

from template_paths import get_template_path
from WenShu.Zhejiang.ELdocx import generate_ELdocx


router = APIRouter()


class EvidenceItem(BaseModel):
    name: str = Field(default="", max_length=300)
    pageCount: str = Field(default="", max_length=20)
    source: str = Field(default="", max_length=200)
    purpose: str = Field(default="", max_length=1000)


class EvidenceRequest(BaseModel):
    committeeName: str = Field(default="", max_length=100)
    caseNumber: str = Field(default="", max_length=80)
    copyCount: int = Field(default=2, ge=1, le=20)
    submitterName: str = Field(default="", max_length=80)
    submitDate: str = ""
    evidenceList: list[EvidenceItem] = Field(default_factory=list, max_length=30)

    @field_validator("evidenceList")
    @classmethod
    def non_empty_items(cls, value: list[EvidenceItem]):
        return value


def _remove_file(path: str):
    try:
        os.remove(path)
    except OSError:
        pass


@router.post("/generate")
async def generate_zhejiang_evidence(req: EvidenceRequest, background_tasks: BackgroundTasks):
    try:
        template_path = get_template_path("《证据清单》.docx", "zhejiang")
        doc = generate_ELdocx(req.model_dump(), template_path)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            doc.save(tmp.name)
            output_path = tmp.name

        background_tasks.add_task(_remove_file, output_path)
        return FileResponse(
            output_path,
            filename="浙江省劳动仲裁证据清单.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Cache-Control": "no-store"},
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="证据清单生成失败，请稍后重试") from exc
