"""Fill the official four-page Guangdong worker arbitration application."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt


def _write_paragraph(paragraph, text: str, *, size: int = 11, align=None):
    for child in list(paragraph._p):
        if child.tag != qn("w:pPr"):
            paragraph._p.remove(child)
    run = paragraph.add_run(str(text or ""))
    run.font.name = "宋体"
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "宋体")
    run.font.size = Pt(size)
    if align is not None:
        paragraph.alignment = align


def _write_cell(cell, text: str, *, size: int = 11, align=WD_ALIGN_PARAGRAPH.LEFT):
    paragraph = cell.paragraphs[0]
    for extra in cell.paragraphs[1:]:
        cell._tc.remove(extra._p)
    _write_paragraph(paragraph, text, size=size, align=align)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def _write_if(cell, value, *, size: int = 11, align=WD_ALIGN_PARAGRAPH.LEFT):
    if str(value or "").strip():
        _write_cell(cell, value, size=size, align=align)


def _format_date(value: str) -> str:
    try:
        parsed = date.fromisoformat(value)
        return f"{parsed.year}年{parsed.month}月{parsed.day}日"
    except (TypeError, ValueError):
        return str(value or "")


def _checkbox(value: str, yes_text: str = "是", no_text: str = "否") -> str:
    if value == yes_text:
        return f"☑{yes_text}  □{no_text}"
    if value == no_text:
        return f"□{yes_text}  ☑{no_text}"
    return f"□{yes_text}  □{no_text}"


def _split_text(value: str, width: int = 32, limit: int = 22) -> list[str]:
    text = str(value or "").replace("\r", "").strip()
    lines: list[str] = []
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        while len(paragraph) > width:
            cut = width
            punctuation = max(paragraph.rfind(mark, max(0, width - 10), width + 1) for mark in "，。；！？")
            if punctuation >= max(0, width - 10):
                cut = punctuation + 1
            while 1 < cut < len(paragraph) and paragraph[cut - 1].isascii() and paragraph[cut - 1].isalnum() and paragraph[cut].isascii() and paragraph[cut].isalnum():
                cut -= 1
            lines.append(paragraph[:cut])
            paragraph = paragraph[cut:]
        if paragraph:
            lines.append(paragraph)
    if len(lines) > limit:
        raise ValueError("事情经过内容过长，请压缩到约900字以内")
    return lines


def generate_LAdocx(data: dict, template_docx: str | Path):
    doc = Document(str(template_docx))

    # Page 1: parties and filing details.
    if data.get("committeeName"):
        _write_paragraph(doc.paragraphs[3], f"致：{data.get('committeeName', '')}", size=12)
    parties = doc.tables[0]
    _write_if(parties.rows[0].cells[1], data.get("applicantName", ""))
    _write_if(parties.rows[0].cells[4], data.get("gender", ""), align=WD_ALIGN_PARAGRAPH.CENTER)
    _write_if(parties.rows[0].cells[7], _format_date(data.get("birthDate", "")), align=WD_ALIGN_PARAGRAPH.CENTER)
    _write_if(parties.rows[1].cells[1], data.get("idNumber", ""))
    _write_if(parties.rows[1].cells[7], data.get("phone", ""), align=WD_ALIGN_PARAGRAPH.CENTER)
    _write_if(parties.rows[2].cells[1], data.get("idAddress", ""))
    applicant_mailing = data.get("applicantMailingAddress") or data.get("idAddress", "")
    if applicant_mailing:
        _write_cell(parties.rows[3].cells[1], f"☑其他：{applicant_mailing}")

    _write_if(parties.rows[4].cells[1], data.get("respondentName", ""))
    _write_if(parties.rows[5].cells[1], data.get("registeredAddress", ""))
    respondent_mailing = data.get("mailingAddress") or data.get("registeredAddress", "")
    if respondent_mailing:
        _write_cell(parties.rows[6].cells[1], f"□与被申请人住所相同\n☑其他：{respondent_mailing}")
    _write_if(parties.rows[7].cells[2], data.get("legalRepName", ""), align=WD_ALIGN_PARAGRAPH.CENTER)
    _write_if(parties.rows[8].cells[2], data.get("legalRepPosition", ""), align=WD_ALIGN_PARAGRAPH.CENTER)
    contact_name = data.get("companyContact") or data.get("legalRepName", "")
    contact_phone = data.get("companyContactPhone") or data.get("legalRepPhone", "")
    contact = " ".join(part for part in (contact_name, contact_phone) if part)
    _write_if(parties.rows[7].cells[6], contact, align=WD_ALIGN_PARAGRAPH.CENTER)
    _write_if(parties.rows[9].cells[1], data.get("applicantName", ""), align=WD_ALIGN_PARAGRAPH.CENTER)
    _write_if(parties.rows[9].cells[6], _format_date(data.get("applicationDate", "")), align=WD_ALIGN_PARAGRAPH.CENTER)

    # Page 2: requests and calculation explanation.
    request_table = doc.tables[1]
    requests = [str(item).strip() for item in data.get("requests", []) if str(item).strip()]
    for index, row_index in enumerate((1, 3, 5, 7)):
        if index < len(requests):
            _write_cell(request_table.rows[row_index].cells[0], f"{index + 1}、")
            _write_cell(request_table.rows[row_index].cells[2], requests[index])
    for index, line in enumerate(_split_text(data.get("claimCalculation", ""), width=32, limit=8)):
        _write_cell(request_table.rows[16 + index].cells[1], line)

    # Page 3: structured basic facts from the official form.
    facts = doc.tables[2]
    _write_if(facts.rows[1].cells[1], _format_date(data.get("employmentDate", "")), align=WD_ALIGN_PARAGRAPH.CENTER)
    _write_if(facts.rows[1].cells[6], data.get("jobTitle", ""), align=WD_ALIGN_PARAGRAPH.CENTER)
    if data.get("signedContract"):
        _write_cell(facts.rows[1].cells[11], _checkbox(data.get("signedContract", ""), "有", "无"), size=10)
    contract_period = "至".join(filter(None, (_format_date(data.get("contractStartDate", "")), _format_date(data.get("contractEndDate", "")))))
    _write_if(facts.rows[2].cells[1], contract_period, align=WD_ALIGN_PARAGRAPH.CENTER)
    _write_if(facts.rows[3].cells[1], data.get("workAddress", ""))
    _write_if(facts.rows[4].cells[1], data.get("workSchedule", ""))
    if data.get("attendanceRequired"):
        _write_cell(facts.rows[5].cells[1], _checkbox(data.get("attendanceRequired", "")), size=10)
    _write_if(facts.rows[5].cells[4], data.get("attendanceMethod", ""), align=WD_ALIGN_PARAGRAPH.CENTER)
    _write_if(facts.rows[5].cells[7], data.get("salaryPaymentMethod", ""), align=WD_ALIGN_PARAGRAPH.CENTER)
    _write_if(facts.rows[5].cells[10], data.get("salaryReceiptRequired", ""), size=10)
    _write_if(facts.rows[6].cells[1], data.get("startingSalary", ""), align=WD_ALIGN_PARAGRAPH.CENTER)
    _write_if(facts.rows[6].cells[6], data.get("salaryAdjustments", ""))
    if data.get("currentlyEmployed"):
        _write_cell(facts.rows[7].cells[2], _checkbox(data.get("currentlyEmployed", "")), size=10)
    _write_if(facts.rows[7].cells[8], _format_date(data.get("departureDate", "")), align=WD_ALIGN_PARAGRAPH.CENTER)
    _write_if(facts.rows[8].cells[4], data.get("departureReason", ""))
    _write_if(facts.rows[9].cells[8], data.get("averageMonthlySalary", ""), align=WD_ALIGN_PARAGRAPH.RIGHT)

    # Page 4: keep the lined layout and distribute the narrative without resizing rows.
    narrative = doc.tables[3]
    for index, line in enumerate(_split_text(data.get("factsReason", ""))):
        _write_cell(narrative.rows[index + 1].cells[1], line)
    return doc
