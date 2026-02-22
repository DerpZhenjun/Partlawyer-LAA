from docx.shared import Pt
from docx.oxml.ns import qn

# 设置宋体小四
def set_font_simsun(run):
    run.font.name = '宋体'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    run.font.size = Pt(12)  # 小四号字体

# 设置 Times New Roman 小四
def set_font_times_new_roman(run):
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)  # 小四号字体

# 设置小四
def twelve_lbs(run):
    run.font.size = Pt(12)