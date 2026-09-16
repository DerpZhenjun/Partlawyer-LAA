from __future__ import annotations

import os
import re
import tempfile
from typing import Literal

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator

from template_paths import get_template_path
from WenShu.Guangdong.LAdocx import generate_LAdocx


router = APIRouter()


class GuangdongApplicationRequest(BaseModel):
    committeeName: str = Field(default="", max_length=100)
    applicantName: str = Field(default="", max_length=80)
    birthDate: str = ""
    gender: Literal["", "男", "女", "其他"] = ""
    nationality: str = Field(default="", max_length=30)
    idNumber: str = Field(default="", max_length=30)
    phone: str = Field(default="", max_length=30)
    householdType: str = Field(default="", max_length=30)
    idAddress: str = Field(default="", max_length=300)
    applicantMailingAddress: str = Field(default="", max_length=300)

    respondentName: str = Field(default="", max_length=200)
    socialCreditCode: str = Field(default="", max_length=30)
    registeredAddress: str = Field(default="", max_length=300)
    mailingAddress: str = Field(default="", max_length=300)
    workAddress: str = Field(default="", max_length=300)
    legalRepName: str = Field(default="", max_length=80)
    legalRepPhone: str = Field(default="", max_length=30)
    legalRepPosition: str = Field(default="", max_length=80)
    companyContact: str = Field(default="", max_length=80)
    companyContactPhone: str = Field(default="", max_length=30)

    requests: list[str] = Field(default_factory=list, max_length=4)
    claimCalculation: str = Field(default="", max_length=240)
    factsReason: str = Field(default="", max_length=700)
    employmentDate: str = ""
    jobTitle: str = Field(default="", max_length=100)
    signedContract: str = Field(default="", max_length=10)
    contractStartDate: str = ""
    contractEndDate: str = ""
    workSchedule: str = Field(default="", max_length=500)
    attendanceRequired: str = Field(default="", max_length=10)
    attendanceMethod: str = Field(default="", max_length=100)
    salaryPaymentMethod: str = Field(default="", max_length=50)
    salaryReceiptRequired: str = Field(default="", max_length=50)
    startingSalary: str = Field(default="", max_length=100)
    salaryAdjustments: str = Field(default="", max_length=500)
    currentlyEmployed: str = Field(default="", max_length=10)
    departureDate: str = ""
    departureReason: str = Field(default="", max_length=1000)
    averageMonthlySalary: str = Field(default="", max_length=100)
    copyCount: int = Field(default=1, ge=1, le=20)
    applicationDate: str = ""

    @field_validator("requests")
    @classmethod
    def validate_requests(cls, value: list[str]):
        cleaned = [item.strip() for item in value if item and item.strip()]
        if any(len(item) > 300 for item in cleaned):
            raise ValueError("单项仲裁请求不能超过300字")
        return cleaned


def _remove_file(path: str):
    try:
        os.remove(path)
    except OSError:
        pass


def _safe_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", name).strip(" .")
    return (cleaned[:60] or "申请人") + "的劳动人事争议仲裁申请书.docx"


@router.post("/generate")
async def generate_guangdong_application(req: GuangdongApplicationRequest, background_tasks: BackgroundTasks):
    try:
        template_path = get_template_path("仲裁申请书.docx", "guangdong")
        doc = generate_LAdocx(req.model_dump(), template_path)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            doc.save(tmp.name)
            output_path = tmp.name

        background_tasks.add_task(_remove_file, output_path)
        return FileResponse(
            output_path,
            filename=_safe_filename(req.applicantName),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Cache-Control": "no-store"},
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail="文书生成失败，请稍后重试") from exc
