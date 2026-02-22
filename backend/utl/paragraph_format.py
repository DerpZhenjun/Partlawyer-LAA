from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Pt

# 设置段落行间距的函数
def set_paragraph_line_spacing(paragraph, spacing_pt):
    """
    设置段落的行间距为固定值。
    
    参数:
    - paragraph: 需要设置行间距的段落对象
    - spacing_pt: 行间距的磅值
    """
    p_format = paragraph.paragraph_format
    p_format.line_spacing = Pt(spacing_pt)  # 设置为固定行距

# 设置段落水平居中的函数
def set_paragraph_center(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

# 设置单元格垂直居中的函数
def set_cell_vertical_center(cell):
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER