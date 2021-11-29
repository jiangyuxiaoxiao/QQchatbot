import sqlite3
from nonebot import on_message,on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot import require
from nonebot.rule import Rule
import datetime
import random
import urllib.request
import os

def sign_in_checker():
    async def inner_sign_in_checker(bot: Bot, event: Event, state: T_State) -> bool:
        if event.post_type == "message":
            if event.message_type == "group":
                msg = event.raw_message
                if msg == "签到":
                    return True
    return Rule(inner_sign_in_checker)

# 调用用户库刷新函数
refresh = require("database_management").refresh

# Handler
daily_sign_in = on_message(priority=60,rule=sign_in_checker(),block=True)


# handle
@daily_sign_in.handle()
async def daily_sign_in(bot: Bot, event: Event, state: T_State):
    # 连接数据库
    connect = sqlite3.connect(".\\Bot_data\\SQLite\\Users.db")
    # 创建游标
    cursor = connect.cursor()

    # 获取用户信息
    user_id = (event.user_id,)

    # 存在性检查
    cursor.execute('''SELECT *
                      FROM USERS
                      WHERE QID = (?)''',user_id)
    if len(list(cursor)) == 0:
        await refresh(bot, event, state)
    # 重复签到查询
    # 当前时间
    date = datetime.date.today()
    date = str(date)
    #查看是否在表中
    cursor.execute('''SELECT LASTSIGN,GOLD,ATTITUDE
                      FROM USERS
                      WHERE QID = (?)''',user_id)
    info = list(cursor)
    bonus = random.randint(0, 100)
    print(bonus)
    add_coin = random.randint(5, 100)
    add_attitude = random.randint(1, 20)
    if bonus == 100:
        add_coin = 1000
        add_attitude = 200
    elif bonus >= 90:
        add_coin = 200
        add_attitude = 40
    coin = add_coin + info[0][1]
    attitude = add_attitude + info[0][2]
    update_pack = (date, coin, attitude, event.user_id)
    user_id = event.user_id
    group_id = event.group_id
    img = ".\\Bot_data\\Image\\atri_daily.jpg"
    img = os.path.abspath(img)
    img = urllib.request.pathname2url(img)
    img = "file:" + img
    # 如果不在表中
    if info[0][0] == None:
        cursor.execute('''UPDATE USERS
                          SET LASTSIGN=(?),GOLD=(?),ATTITUDE=(?)
                          WHERE QID = (?)''',update_pack)
    elif info[0][0] == date:
        msg = "[CQ:at,qq={}]你今天已经签到过了哦".format(user_id)
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
        return
    else:
        cursor.execute('''UPDATE USERS
                          SET LASTSIGN=(?),GOLD=(?),ATTITUDE=(?)
                          WHERE QID = (?)''',update_pack)
    # 提交数据，关闭连接
    connect.commit()
    cursor.close()
    connect.close()
    if bonus < 90:
        msg = "[CQ:at,qq={}]签到成功~\n获得{}枚托莉币，当前托莉币{}。\n好感度+{}，当前好感度{}" \
        "[CQ:image,file={}]".format(user_id,add_coin,coin,add_attitude,attitude,img)
    elif bonus < 100:
        img = ".\\Bot_data\\Image\\atri_yes1.png"
        img = os.path.abspath(img)
        img = urllib.request.pathname2url(img)
        img = "file:" + img
        msg = "[CQ:at,qq={}]签到大成功！(10%）\n获得{}枚托莉币，当前托莉币{}。\n好感度+{}，当前好感度{}" \
              "[CQ:image,file={}]".format(user_id, add_coin, coin, add_attitude, attitude, img)
    elif bonus == 100:
        img = ".\\Bot_data\\Image\\atri10.jpg"
        img = os.path.abspath(img)
        img = urllib.request.pathname2url(img)
        img = "file:" + img
        msg = "[CQ:at,qq={}]签到大大成功！(1%）可恶！又被秀到了\n获得{}枚托莉币，当前托莉币{}。\n好感度+{}，当前好感度{}" \
              "[CQ:image,file={}]".format(user_id, add_coin, coin, add_attitude, attitude, img)
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})





