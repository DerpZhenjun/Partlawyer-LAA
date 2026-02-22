import json

def txt_to_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # 使用.rstrip('\n')方法移除每行末尾的换行符，并且使用条件推导式来移除空行
        lines = [line.rstrip('\n') for line in f.readlines() if line.strip()]
    q_a_data = [{'question': lines[i], 'answer': lines[i + 1]} for i in range(0, len(lines), 2)]
    with open(r'D:\Programming\WenshuWebsite\project1\partlawyer1\data\json\partlawyer1_version1.json', 'w', encoding='utf-8') as f:
        json.dump(q_a_data, f, ensure_ascii=False, indent=4)

txt_to_json(r'D:\Programming\WenshuWebsite\partlawyer\data\txt\partlawyer1_version1.txt')