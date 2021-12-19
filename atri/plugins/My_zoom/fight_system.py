import json
import sqlite3
import random
import time

commondb = "./Bot_data/My_zoom/common.db"
indexfile = "./Bot_data/My_zoom/pat.json"
indexfile_2 = "./Bot_data/My_zoom/get_pat.json"
indexfile3 = "./Bot_data/My_zoom/fight_parameter.json"


def query_pet(user_id):
    # 连接数据库并且找到对战双方的宠物信息
    connect = sqlite3.connect(commondb)
    cursor = connect.cursor()
    cursor.execute("select * from user where id={}".format(user_id))
    response = cursor.fetchall()
    # 关闭连接
    cursor.close()
    connect.close()
    pet = response[0][2:-1]
    have_pet = False
    for pet_number in pet:
        if pet_number != 0:
            have_pet = True
    if have_pet:
        return list(pet)
    else:
        return False


# 单个宠物的战斗
def pet_fight(pet_1, pet_2):
    with open(indexfile, encoding="utf-8") as fp:
        index = json.load(fp)
        data = index['data']
        data = data[2:]
        # print(index[data[pet_1]],index[data[pet_2]])
        player1 = index[data[pet_1]]
        player2 = index[data[pet_2]]
        print('ok1')

    with open(indexfile3, encoding="utf-8") as fp:
        index = json.load(fp)
        ROI = index["Ratio_of_injury"]
        print('ok2')

    # 初始化
    message = []

    speed1 = player1["speed"]
    speed2 = player2["speed"]
    img1 = player1["img"]
    img2 = player2["img"]

    print(player2['img'])
    death = 0
    sit = 0
    # 战斗采取回合制，每一次循环都是一个回合
    while True:
        # 根据速度决定先后手
        if player1["speed"] >= player2["speed"]:
            first = player1
            last = player2
            first_speed = speed1
            last_speed = speed2
            sit = 1  # 表示玩家1先手
            # msg = "{}向{}发起了攻击！".format(img1, img2)
            # message.append(msg)
            print('ok4')
        else:
            first = player2
            last = player1
            first_speed = speed2
            last_speed = speed1
            sit = 2  # 表示玩家2先手
            # msg = "{}向{}发起了攻击！".format(img2, img1)
            # message.append(msg)
            print('ok4')

        # 随机数生成是否闪避
        avoid = random.randint(1, 100)
        if avoid <= last["avoid"]:
            print('闪避成功')
            if sit == 1:
                msg = "{}闪避了{}的攻击，真漂亮！".format(img2, img1)
                message.append(msg)
                player1["speed"] = (player1["speed"] + speed1 - speed2) % speed1
                continue
            else:
                msg = "{}闪避了{}的攻击，真漂亮！".format(img1, img2)
                message.append(msg)
                player2["speed"] = (player2["speed"] + speed2 - speed1) % speed2
                continue

        # 闪避失败
        injury = first["damage"] - last["defense"]
        if injury < 0:
            injury = 0
        # print(last['blood'])
        last["blood"] = last["blood"] - injury
        msg = "{}受到了来自{}的{}点伤害\n当前血量为：{}".format(last['img'],
                                                 first['img'],
                                                 injury, last['blood'])
        # print(last['blood'])
        message.append(msg)

        # 结算本回合
        first["speed"] = (first["speed"] + first_speed - last_speed) % first_speed

        # 如果有宠物战死
        if last["blood"] <= 0:
            last["blood"]=0
            if sit == 1:
                death = 2
            else:
                death = 1
            break
        #如果没有宠物战死
        if sit == 1:
            player1 = first
            player2 = last
        else:
            player1 = last
            player2 = first
    return message, death


def fight(player1, player2):
    pet_1 = query_pet(player1)
    # print("pet1:", pet_1)
    pet_2 = query_pet(player2)
    # print("pet2:", pet_2)
    if not pet_1:
        return ["挑战者没有宠物可以参战。", ]
    if not pet_2:
        return ["对方没有宠物可以参战。", ]
    with open(indexfile, encoding="utf-8") as fp:
        index = json.load(fp)
        data = index["data"][2:]
        name = index["name"]
        # print(data, name)

    message = []
    msg = "战斗开始。\n右边是被挑战者，左边是挑战者。"
    message.append(msg)

    loser=""
    while True:
        p1 = 0
        p2 = 0
        for pt1 in pet_1:
            if pt1 != 0:
                break
            else:
                p1 += 1
        for pt2 in pet_2:
            if pt2 != 0:
                break
            else:
                p2 += 1

        msg = "{}  vs  {}!".format(name[p1], name[p2])
        message.append(msg)

        msg_ext, result = pet_fight(pet_1=p1, pet_2=p2)
        message.extend(msg_ext)

        if result ==1:
            pet_1[p1]=pet_1[p1]-1
        else:
            pet_2[p2]=pet_2[p2]-1

        player1_alive=False
        player2_alive=False
        for pt1 in pet_1:
            if pt1 !=0:
                player1_alive=True
        for pt2 in pet_2:
            if pt2 !=0:
                player2_alive=True

        if not player2_alive:
            loser=player2
            msg="挑战成功！"
            message.append(msg)
            break
        if not player1_alive:
            loser=player1
            msg="挑战失败！"
            message.append(msg)
            break
    return message
