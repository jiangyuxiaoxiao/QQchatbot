import json

dictionary = {}

indexname = "./Bot_data/Dictionary/index.json"


def dictionary_initial():
    # 读取词库目录索引文件
    with open(indexname, encoding="utf-8") as index_file:
        index = json.load(index_file)
        index = index['index']
        print(index)

        # 遍历读取每个词库
        for dictionary_name in index:
            dictionary_file = "./Bot_data/Dictionary/" + dictionary_name + ".json"
            with open(dictionary_file, encoding="utf-8") as dict_file:
                dict_piece = json.load(dict_file)
                # 遍历插入字典
                for sentence in dict_piece:
                    # 防止词库冲突 先加载的词库优先级高，不会被后加载的词库覆盖
                    if sentence not in dictionary:
                        dictionary[sentence] = dict_piece[sentence]

        print("当前词条数: " + str(len(dictionary)))

