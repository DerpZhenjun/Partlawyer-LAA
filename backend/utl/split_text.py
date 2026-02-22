import re

def split_text_by_length_and_newline(text, length):
    """
    将文本按指定规则分割为多个部分，考虑换行符和特殊的字符计数规则。
    
    规则如下：
    - 优先按换行符（\r）分割文本。
    - 每个分割后的块再按以下规则计算长度和分割：
      - 连续的1到2个数字算作一个字符。
      - 连续的1到2个小写字母算作一个字符。
      - 其他字符（如汉字、标点符号等）算作一个字符。
    
    参数:
    - text: 需要分割的文本
    - length: 每部分的最大"字符"数
    
    返回:
    - 分割后的文本列表
    """
    # 首先按换行符分割
    chunks = text.split('\r')
    result = []
    
    for chunk in chunks:
        # 使用正则表达式将每个块分割为"计算单元"
        pattern = r'\d{1,2}|[a-z]{1,2}|.'
        units = re.findall(pattern, chunk)
        
        current_part = ""
        current_length = 0
        
        for unit in units:
            # 对于数字序列和小写字母序列，长度算作1
            if unit.isdigit() or (unit.islower() and len(unit) <= 2):
                unit_length = 1
            else:
                unit_length = len(unit)
            
            if current_length + unit_length > length:
                result.append(current_part)
                current_part = unit
                current_length = unit_length
            else:
                current_part += unit
                current_length += unit_length
        
        # 添加最后一部分
        if current_part:
            result.append(current_part)
    
    return result

# # 测试函数
# t1 = '（1）请求确认2018年8月20日至2018年11月19日期间双方存在劳动关系；'
# t2 = split_text_by_length_and_newline(t1, 32)
# print(t2)