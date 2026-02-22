from utl.font_format import set_font_simsun
from utl.font_format import set_font_times_new_roman

def is_digital_or_letter(char):
    return char.isdigit() or char.isalpha()

# 根据内容设置字体
def apply_font_based_on_content(cell, text, paragraphs_num):
    for char in text:
        run = cell.paragraphs[paragraphs_num].add_run(char)
        if is_digital_or_letter(char):
            set_font_times_new_roman(run)
        else:
            set_font_simsun(run)