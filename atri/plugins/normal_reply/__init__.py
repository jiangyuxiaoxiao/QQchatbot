import random
import urllib.request
import os
from nonebot import on_message
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from load_dictionary import dictionary
from nonebot.plugin import require
import sqlite3
# 引用字典
import sys
sys.path.append("../../")

# 调用用户库刷新函数
refresh = require("database_management").refresh

# 注册一个事件响应器，事件类型为message.
reply = on_message(priority = 500, block=False)


# 全匹配回复
@reply.handle()
async def normal_reply(bot: Bot, event: Event, state: T_State):
    event_msg = event.raw_message
    message_type = ""
    # 群聊信息标志
    if event.message_type == 'group':
        message_type = 'group'
        group_id = event.group_id
        user_id = (event.user_id,)
    # 私聊信息标志
    if event.message_type == 'private':
        message_type = 'private'
        user_id = (event.user_id,)
    # 只在群聊和私聊中触发
    if message_type == 'group' or message_type == 'private':
        # 数据库检索
        # 连接数据库
        connect = sqlite3.connect("./Bot_data/SQLite/Users.db")
        # 创建游标
        cursor = connect.cursor()
        # 搜索好感度
        cursor.execute(
            '''
            SELECT *
            FROM USERS
            WHERE QID = (?)
            ''', user_id
        )
        info = list(cursor)

        # 用户列表审查 如果不存在则先执行刷新
        if len(info) == 0:
            cursor.close()
            connect.close()
            await refresh(bot, event, state)
            connect = sqlite3.connect("./Bot_data/SQLite/Users.db")
            cursor = connect.cursor()
            # 搜索好感度
            cursor.execute(
                '''
                SELECT *
                FROM USERS
                WHERE QID = (?)
                ''', user_id
            )
            info = list(cursor)

        # 数据库提取信息
        attitude = info[0][2]
        # 断开连接
        cursor.close()
        connect.close()

        # 应该先确定是否有key匹配的 然后精确搜索范围
        for key in dictionary:
            # 关键词在语句中
            if key in event_msg:
                is_keyword = 0
                # 如果是关键字型触发
                if not event_msg == key:
                    is_keyword = 1

                # 从上至下寻找符合条件的回复
                for reply in dictionary[key]:
                    # 检查是否需要@
                    if reply["need_at"] == True:
                        if not event.to_me:
                            continue
                    # 检查好感度
                    if reply["need_attitude"] > attitude:
                        continue
                    # 检查是否是关键字
                    if is_keyword == 1:
                        if reply["is_keyword"] == False:
                            continue

                    # 若有多个匹配则随机挑选
                    msgs = reply["msg"]
                    msgnum = random.randint(0, len(msgs)-1)
                    msg = msgs[msgnum]

                    # 检查是否有图片
                    if not reply["img"] == "":
                        img = "./Bot_data/Image/" + reply["img"]
                        img = os.path.abspath(img)
                        img = urllib.request.pathname2url(img)
                        img = "file:" + img
                        print(img)
                        msg = msg + "[CQ:image,file={}]".format(img)

                    # 检查是否有语音
                    if not reply["sound"] == "":
                        sound = "./Bot_data/Sound/Sound/" + reply["sound"]
                        sound = os.path.abspath(sound)
                        sound = urllib.request.pathname2url(sound)
                        sound = "file:" + sound
                        msg2 =  "[CQ:record,file={}]".format(sound)

                    # 如果是群聊
                    if message_type == 'group':
                        group_id = event.group_id
                        print(msg,group_id)
                        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
                        if not reply["sound"] == "":
                            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg2})
                    else:
                        print(msg, user_id)
                        await bot.call_api("send_private_msg", **{"user_id": user_id, "message": msg})
                        if not reply["sound"] == "":
                            await bot.call_api("send_private_msg", **{"user_id": user_id, "message": msg})
                    break  # 只回复好感度最高的一句
        return
