import sqlite3
from nonebot import on_message,on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot import require
from nonebot.exception import StopPropagation


# 阻断command
black_list_checker_command = on_command("",priority = 0,block=False)
# 阻断message
black_list_checker_message = on_message(priority = 0,block=False)
# 设置黑名单
set_black_list_on_command = on_command("设置黑名单", priority = 0, block=True)
# 设置群黑名单
set_group_black_list_on_command = on_command("设置群黑名单", priority = 0, block=True)

# 调用用户库刷新函数
refresh = require("database_management").refresh

@black_list_checker_command.handle()
async def black_list_checker_command(bot: Bot, event: Event, state: T_State):
    connect = sqlite3.connect(".\\Bot_data\\SQLite\\Users.db")
    # 创建游标
    cursor = connect.cursor()

    # 对于群聊消息
    if event.message_type == "group":
        group_id = (event.group_id,)
        user_id = (event.user_id,)

        # 判断群是否在黑名单
        cursor.execute('''SELECT *
                          FROM GROUPS
                          WHERE GROUPID = (?)  ''',group_id)
        info = list(cursor)
        if len(info) == 0:
            await refresh(bot, event, state)
            # 不在数据库里的一般不在黑名单
            cursor.close()
            connect.close()
            return
        else:
            info = info[0][1]
            # 在黑名单中
            if info == 3:
                cursor.close()
                connect.close()
                raise StopPropagation

        # 判断用户是否在黑名单
        cursor.execute('''SELECT *
                          FROM USERS
                          WHERE QID = (?)  ''', user_id)
        info = list(cursor)
        if len(info) == 0:
            await refresh(bot, event, state)
            # 不在数据库里的一般不在黑名单
            cursor.close()
            connect.close()
            return
        else:
            info = info[0][1]
            # 在黑名单中
            if info == 3:
                cursor.close()
                connect.close()
                raise StopPropagation

    elif event.message_type == "private":
        # 基本上复制即可
        user_id = (event.user_id,)
        # 判断用户是否在黑名单
        cursor.execute('''SELECT *
                          FROM USERS
                          WHERE QID = (?)  ''', user_id)
        info = list(cursor)
        if len(info) == 0:
            await refresh(bot, event, state)
            # 不在数据库里的一般不在黑名单
            cursor.close()
            connect.close()
            return
        else:
            info = info[0][1]
            # 在黑名单中
            if info == 3:
                cursor.close()
                connect.close()
                raise StopPropagation
    cursor.close()
    connect.close()


@black_list_checker_message.handle()
async def black_list_checker_message(bot: Bot, event: Event, state: T_State):
    connect = sqlite3.connect(".\\Bot_data\\SQLite\\Users.db")
    # 创建游标
    cursor = connect.cursor()

    # 对于群聊消息
    if event.message_type == "group":
        group_id = (event.group_id,)
        user_id = (event.user_id,)

        # 判断群是否在黑名单
        cursor.execute('''SELECT *
                          FROM GROUPS
                          WHERE GROUPID = (?)  ''',group_id)
        info = list(cursor)
        if len(info) == 0:
            await refresh(bot, event, state)
            # 不在数据库里的一般不在黑名单
            cursor.close()
            connect.close()
            return
        else:
            info = info[0][1]
            # 在黑名单中
            if info == 3:
                cursor.close()
                connect.close()
                raise StopPropagation

        # 判断用户是否在黑名单
        cursor.execute('''SELECT *
                          FROM USERS
                          WHERE QID = (?)  ''', user_id)
        info = list(cursor)
        if len(info) == 0:
            await refresh(bot, event, state)
            # 不在数据库里的一般不在黑名单
            cursor.close()
            connect.close()
            return
        else:
            info = info[0][1]
            # 在黑名单中
            if info == 3:
                cursor.close()
                connect.close()
                raise StopPropagation

    elif event.message_type == "private":
        # 基本上复制即可
        user_id = (event.user_id,)
        # 判断用户是否在黑名单
        cursor.execute('''SELECT *
                          FROM USERS
                          WHERE QID = (?)  ''', user_id)
        info = list(cursor)
        if len(info) == 0:
            await refresh(bot, event, state)
            # 不在数据库里的一般不在黑名单
            cursor.close()
            connect.close()
            return
        else:
            info = info[0][1]
            # 在黑名单中
            if info == 3:
                cursor.close()
                connect.close()
                raise StopPropagation
    cursor.close()
    connect.close()


@set_black_list_on_command.handle()
async def set_black_list_1(bot: Bot, event: Event, state: T_State):
    # 权限审查
    user_id = (event.user_id,)
    connect = sqlite3.connect(".\\Bot_data\\SQLite\\Users.db")
    # 创建游标
    cursor = connect.cursor()
    cursor.execute('''SELECT PERMISSION
                      FROM USERS
                      WHERE QID = (?)''',user_id)
    # 权限审核
    info = list(cursor)
    if len(info) == 0:
        await refresh(bot, event, state)
        cursor.execute('''SELECT PERMISSION
                          FROM USERS
                          WHERE QID = (?)''', user_id)
    if not info[0][0] == 0:
        cursor.close()
        connect.close()
        raise StopPropagation

    # 只在群聊中处理该事件
    if event.message_type == "group":
        message = str(event.message)
        group_id = event.group_id
        if not message == "":
            state["QID"] = message
    cursor.close()
    connect.close()

@set_black_list_on_command.got("QID")
async def set_black_list_2(bot: Bot, event: Event, state: T_State):
    QID = state["QID"]
    QID = QID.replace("[CQ:at,qq=", "")
    QID = QID.replace("]", "")
    QID = int(QID)
    user_id =(QID,)
    connect = sqlite3.connect(".\\Bot_data\\SQLite\\Users.db")
    # 创建游标
    cursor = connect.cursor()
    cursor.execute('''SELECT *
                      FROM USERS
                      WHERE QID = (?)''', user_id)
    # 如果不存在：
    info = list(cursor)
    if len(info) == 0:
        await refresh(bot, event, state)
        cursor.execute('''SELECT *
                          FROM USERS
                          WHERE QID = (?)''', user_id)

    cursor.execute('''UPDATE USERS
                      SET PERMISSION = 3
                      WHERE QID = (?)''', user_id)
    connect.commit()
    cursor.close()
    connect.close()
    msg = "设置成功"
    group_id = event.group_id
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})


@set_group_black_list_on_command.handle()
async def set_group_black_list(bot: Bot, event: Event, state: T_State):
    if event.message_type == "group":
        group_id = (event.group_id,)
        user_id = (event.user_id,)
        connect = sqlite3.connect(".\\Bot_data\\SQLite\\Users.db")
        # 创建游标
        cursor = connect.cursor()
        cursor.execute('''SELECT PERMISSION
                          FROM USERS
                          WHERE QID = (?)''', user_id)
        # 权限审核
        info = list(cursor)
        if len(info) == 0:
            await refresh(bot, event, state)
            cursor.execute('''SELECT PERMISSION
                              FROM USERS
                              WHERE QID = (?)''', user_id)
        if not info[0][0] == 0:
            cursor.close()
            connect.close()
            return

        # 检查群是否在表中
            # 判断群是否在黑名单
        cursor.execute('''SELECT *
                          FROM GROUPS
                          WHERE GROUPID = (?)  ''', group_id)
        info = list(cursor)
        if len(info) == 0:
            await refresh(bot, event, state)
        # 设置黑名单
        cursor.execute('''UPDATE GROUPS
                          SET PERMISSION = 3
                          WHERE GROUPID = (?)''', group_id)
        connect.commit()
        cursor.close()
        connect.close()
        msg = "设置成功"
        group_id = event.group_id
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})



