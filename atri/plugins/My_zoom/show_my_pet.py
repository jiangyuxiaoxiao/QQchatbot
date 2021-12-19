import json
import sqlite3

commondb = ".\\Bot_data\\My_zoom\\common.db"
indexfile = ".\\Bot_data\\My_zoom\\pat.json"


def show_pet(user_id):
    # 连接数据库
    connect = sqlite3.connect(commondb)
    sursor = connect.cursor()
    sursor.execute("select * from user where id={}".format(user_id))
    response = sursor.fetchall()
    response = response[0]
    print(response)

    if not response:
        print("error")
        return "你还未加入宠物乐园，请先注册！"

    # 打开json文件
    with open(indexfile, encoding="utf-8") as fp:
        index = json.load(fp)
        index = index["name"]
        # print(index)

    # 建立列表message保存要发送的消息
    message = []
    name=response[1]+':\n'
    msg = response[1] + ":\n"
    msg = msg + "你的宠物如下：\n"
    message.append(msg)

    response = response[2:-1]
    # print(response)
    # 有几个宠物就输出几次宠物，每次最多输出十个宠物
    i = 0
    for res in response:
        msg = name
        x = 1
        while x <= res:
            msg = msg + index[i]
            x += 1
            if x % 10 == 0 and x<res:
                message.append(msg)
                msg = name
        if msg!=name:
            message.append(msg)
        i += 1
    return message
