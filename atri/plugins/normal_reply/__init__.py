import random

from nonebot import on_message
from nonebot.rule import to_me
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


@reply.handle()
async def normal_reply(bot: Bot, event: Event, state: T_State):
    msg = event.raw_message
    if msg in dictionary:
        if event.message_type == 'group':
            group_id = event.group_id
            user_id = (event.user_id,)
            # 连接数据库
            connect = sqlite3.connect(".\\Bot_data\\SQLite\\Users.db")
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
                await refresh(bot,event,state)
                connect = sqlite3.connect(".\\Bot_data\\SQLite\\Users.db")
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
            # 从上至下寻找符合条件的回复
            for reply in dictionary[msg]:
                # 确定好感度是否满足
                if attitude >= reply["need_attitude"]:
                    # 确定是否需要@
                    if reply["need_at"] == True:
                        if not to_me(): continue
                    else:
                        msgs = reply["msg"]
                        msgnumber = random.randint(0, len(msgs))
                        msg = msgs[msgnumber]
                        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
                        break
        return
