import re

def num_to_chinese_upper(group):
    chinese_upper = {'0':'零', '1':'壹', '2':'贰', '3':'叁', '4':'肆', '5':'伍', '6':'陆', '7':'柒', '8':'捌', '9':'玖', '10':'拾'}
    total_units = ['仟', '佰', '拾', '']
    
    result = ''
    units = total_units[-1:-len(group)-1:-1]
    units = units[::-1]
    
    for index, single_number in enumerate(group):
        chinese = chinese_upper[single_number]
        unit = units[index]
        result = result + chinese + (unit if chinese != '零' else '')
    if '零零' in result:
        result = re.sub('零+', '零', result)
    return result.rstrip('零')

def group_num(num_str):
    groups = []
    while len(num_str) > 0:
        group = num_str[-4:]
        groups.append(group)
        num_str = num_str[:-4]
    groups.reverse()
    return groups

def add_unit(finally_numlist):
    finally_num = []
    units = ["", "万", "亿"]
    for unit, upper_num in enumerate(reversed(finally_numlist)):
        unitupper_num = upper_num + units[unit]
        finally_num.append(unitupper_num)
    finally_num = finally_num[::-1]
    finally_num = ''.join(finally_num)
    return finally_num

def num_to_upper_main(num):      
    num_str = str(num)
    groups = group_num(num_str)
    finally_numlist = []
    for group in groups:
        result = num_to_chinese_upper(group)
        finally_numlist.append(result)
    finally_num = add_unit(finally_numlist)
    return finally_num


