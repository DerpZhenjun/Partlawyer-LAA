"""Resolve official document templates from the repository-level template directory."""

from __future__ import annotations

import os
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE_ROOT = REPOSITORY_ROOT / "templates_docx"


PROVINCE_DIRECTORIES = {
    "zhejiang": "ZheJiangSheng",
    "guangdong": "GuangDongSheng",
}


def get_template_path(filename: str, province: str | None = None) -> Path:
    template_root = Path(
        os.getenv("LABOURLAWYER_TEMPLATE_DIR", str(DEFAULT_TEMPLATE_ROOT))
    ).expanduser().resolve()
    province_dir = PROVINCE_DIRECTORIES.get((province or "").lower())
    if province and not province_dir:
        raise ValueError("不支持的省份模板目录")

    template_path = (template_root / province_dir / filename).resolve() if province_dir else (template_root / filename).resolve()

    allowed_parent = (template_root / province_dir).resolve() if province_dir else template_root
    if template_path.parent != allowed_parent:
        raise ValueError("模板文件名不合法")
    if not template_path.is_file():
        raise FileNotFoundError(f"未找到官方文书模板：{template_path}")
    return template_path
