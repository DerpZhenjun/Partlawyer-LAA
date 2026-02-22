from toTuple import get_dataset_questions

# 生成问题的所有可能的同义词替换版本
def generate_all_synonyms(question, synonyms_dictionary):
    all_versions = [question]
    for word, synonyms in synonyms_dictionary.items():
        # print('synonyms_dictionary.items(): ', synonyms_dictionary.items())
        # print('word, synonyms', word, synonyms)
        if word in question:
            all_versions += [question.replace(word, synonym) for synonym in synonyms if synonym != word]
            # print('all_versions: ',all_versions)
    return all_versions

# 生成正负对
def generate_pairs(dataset_questions, synonyms_dictionary):
    positive_pairs = []
    negative_pairs = []
    all_augmented = []

    # 生成正例对
    for question in dataset_questions:
        all_versions = generate_all_synonyms(question, synonyms_dictionary) # 原始问句与其增强问句的组成
        # print('all_versions: ',all_versions)
        all_augmented += all_versions[1:]  # 原始问句除外, 所有增强问句组成增强问句列表
        # print('all_augmented: ',all_augmented)
        positive_pairs += [(question, v) for v in all_versions[1:]]

    # 生成负例对
    for original_q in dataset_questions:
        for q in dataset_questions:
            if q != original_q and q not in generate_all_synonyms(original_q, synonyms_dictionary):
                negative_pairs.append((original_q, q))
        for aug_q in all_augmented:
            if aug_q not in generate_all_synonyms(original_q, synonyms_dictionary):
                negative_pairs.append((original_q, aug_q))
    
    return positive_pairs, negative_pairs

# 问题数据集
dataset_questions = get_dataset_questions()

synonyms_dictionary = {
    "是什么": ["是什么", "是什么意思"],
    "怎么填": ["怎么填", "填什么"],
}

positive_pairs, negative_pairs = generate_pairs(dataset_questions, synonyms_dictionary)

# Output a sample of the generated pairs for verification.
print("Positive pairs (sample):", positive_pairs)
print("Negative pairs (sample):", negative_pairs)