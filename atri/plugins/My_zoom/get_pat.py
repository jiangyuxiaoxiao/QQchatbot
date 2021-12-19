import json
import sqlite3
import random
import time

commondb = './Bot_data/My_zoom/common.db'
indexfile = './Bot_data/My_zoom/get_pat.json'


def get_a_new_pat(id):
    # 获取随机数，抽宠物
    get_rate = random.randint(1, 100)
    # 连接数据库
    connect = sqlite3.connect(commondb)
    # 创建游标
    cursor = connect.cursor()
    # 查询id
    cursor.execute("select * from user where id={}".format(id))
    response = cursor.fetchall()
    print(response)

    if not response:
        print("error")
        return "你还未加入宠物乐园，请先注册！"

    now_date = time.strftime("%Y-%m-%d", time.localtime())
    now_date=int(now_date.replace("-",""))
    print(now_date,type(now_date))
    print(response[0][-1])
    if response[0][-1] == now_date:
        return '''
        你今天已经获取过宠物
        请明天再来试试手气吧'''

    with open(indexfile, encoding="utf-8") as index_file:
        index = json.load(index_file)
        rate = index["rate"]
        pet = index["pet"]
        print(rate, pet)

    r_sum = 0
    i = 0
    while i < len(rate):
        r_sum += rate[i]
        # 根据随机数判断获取的宠物是什么
        if get_rate < r_sum:
            # 如果在概率内，就获取相应的宠物
            # 保存宠物数量在数据库中
            cursor.execute("update user set {}={} where id={}".format(pet["list"][i],
                                                                      response[0][2 + i] + 1,
                                                                      id))
            # 保存当前玩家今天已经抽过卡
            cursor.execute("update user set last_get={} where id={}".format(now_date,
                                                                            id))
            # 测试是否添加成功
            # cursor.execute("select * from user".format(id))
            # response = cursor.fetchall()
            # print(response)

            # 更新数据库
            connect.commit()
            cursor.close()
            connect.close()
            return '''
            🎊🎊🎉🎉🎊🎊
            锵锵锵~~
            恭喜获得一只{}！
            {}~~{}~~~'''.format(pet["name"][i],
                                pet["img"][i],
                                pet["sound"][i])
        if get_rate == r_sum:
            # 抽卡暴击的情况
            cursor.execute("update user set {}={} where id={}".format(pet["list"][i],
                                                                      response[0][2 + i] + 1,
                                                                      id))
            # 保存当前玩家今天已经抽过卡
            cursor.execute("update user set last_get={} where id={}".format(now_date,
                                                                            id))
            # 更新数据库
            connect.commit()
            cursor.close()
            connect.close()
            return '''
            🎊🎊🎉🎉🎊🎊
            震惊！！
            天运之子出现了！
            吸吸欧气！！！
            恭喜获得两只{}!
            {}{}
            ~~{}~~~'''.format(pet["name"][i],
                              pet["img"][i],
                              pet["img"][i],
                              pet["sound"][i])
        i += 1

    cursor.execute("update user set last_get={} where id={}".format(now_date,
                                                                    id))

    cursor.execute(f"select coins from bag where id={id}")
    now_coins=cursor.fetchall()
    now_coins=now_coins[0][0]
    now_coins+=get_rate

    cursor.execute(f"update bag set coins={now_coins} where id={id}")
    connect.commit()
    cursor.close()
    connect.close()
    return f'''
    很遗憾，什么都没有得到。
    但是捡到了{get_rate}个金币！
    快存起来去商城看看吧！
    明天再来试试吧。'''
