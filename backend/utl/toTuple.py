import json

def get_dataset_questions():
    # 将 'path_to_your_file.json' 替换为你的JSON文件的实际文件路径
    file_path = r'D:\Programming\WenshuWebsite\Partlawyer_Legaldocx\data\json\partlawyer1_version1.json'

    # 打开文件并读取其内容
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 现在 data 变量包含了JSON文件中的数据
    # 你可以对这些数据进行进一步的处理，例如提取问题列表
    questions_list = [item["question"] for item in data]
    
    return questions_list

# questions_list = get_dataset_questions()
# print(questions_list)