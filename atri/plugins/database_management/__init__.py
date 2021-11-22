# -*- coding:utf-8 -*-
import nonebot
from nonebot import require
from nonebot import export
import sqlite3
import asyncio
from nonebot import on_command
from nonebot import on_notice
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event

# 定时器
scheduler = require("nonebot_plugin_apscheduler").scheduler
# 群事件处理
group_handler = on_notice(priority=3, block=False)
# 指令处理
command_handler = on_command("数据库刷新", priority=3, block= False)


# 定期更新数据库 更新群列表及用户列表
# 为定期执行的任务，执行时间为传入的hour minute参数
@scheduler.scheduled_job("cron", hour="00", minute="00")
async def update_usersdata():
    # 传入bot对象
    bot = nonebot.get_bot()
    # 连接数据库
    connect = sqlite3.connect(".\\Bot_data\\SQLite\\Users.db")
    # 创建游标
    cursor = connect.cursor()
    # 群组用户更新 群更新
    # 遍历群组
    groups = await bot.call_api("get_group_list")
    # groups为群组列表
    for group in groups:
        # group_id 群号
        group_id = group["group_id"]
        # group_name 群名
        group_name = group["group_name"]
        group_id_tuple = (group_name,)
        # 群更新
        # 查找数据库中是否存在该群
        cursor.execute("SELECT COUNT(*) FROM GROUPS WHERE GROUPID=(?)",group_id_tuple)
        for c in cursor:
            if c[0] == 0:
                insert_value = (group_id, group_name)
                cursor.execute('''
                                INSERT INTO
                                GROUPS(GROUPID,PERMISSION,GROUPNAME)
                                VALUES (?,1,?)
                                ''', insert_value)

        # 群用户更新
        # group_member 群成员列表
        group_members = await bot.call_api("get_group_member_list", **{"group_id": group_id})
        for group_member in group_members:
            # member_id 群成员QQ号
            member_id = group_member["user_id"]
            # 将member_id放入元组中进行数据传入
            member_id_tuple = (member_id,)
            # member_name 群成员QQ名
            member_name = group_member["nickname"]
            # 查找数据库中是否存在该成员
            cursor.execute("SELECT COUNT(*) FROM USERS WHERE QID=(?);", member_id_tuple)
            for c in cursor:
                if c[0] == 0:
                    # 避免SQL注入攻击，使用？来代替字符串替换
                    insert_value = (member_id, member_name)
                    connect.execute('''
                                    INSERT INTO 
                                    USERS(PERMISSION,ATTITUDE,GOLD,QID,QQNAME) 
                                    VALUES(2,0,0,?,?);
                                    ''', insert_value)

    # 好友用户更新 api返回json数组 详见go—cqhttp的文档
    friends = await bot.call_api("get_friend_list")
    for friend in friends:
        # 好友QQ
        friend_id = friend["user_id"]
        # 好友名
        friend_name = friend["nickname"]
        # 查找数据库中是否存在该成员
        cursor.execute("SELECT COUNT(*) FROM USERS WHERE QID=(?);", member_id_tuple)
        for c in cursor:
            if c[0] == 0:
                # 避免SQL注入攻击，使用？来代替字符串替换
                insert_value = (friend_id, friend_name)
                connect.execute('''
                                INSERT INTO 
                                USERS(PERMISSION,ATTITUDE,GOLD,QID,QQNAME) 
                                VALUES(2,0,0,?,?);
                                ''', insert_value)
    # 数据库保存更新
    cursor.close()
    connect.commit()
    connect.close()


# 当群内新增成员时进行处理
@group_handler.handle()
async def add_member_to_user_database(bot: Bot, event: Event, state: T_State):
    if event.notice_type == 'group_increase':
        # 群号
        group_id = event.group_id
        # 进群者QQ号 QQ名
        member_id = event.user_id
        # 将member_id放入元组中进行数据传入
        member_id_tuple = (member_id,)
        info = await bot.call_api("get_group_member_info", **{"group_id": group_id, "user_id": member_id})
        member_name = info["nickname"]
        # 连接数据库
        connect = sqlite3.connect(".\\Bot_data\\SQLite\\Users.db")
        # 创建游标
        cursor = connect.cursor()
        # 判断是否已在数据库内
        cursor.execute("SELECT COUNT(*) FROM USERS WHERE QID=(?);", member_id_tuple)
        for c in cursor:
            if c[0] == 0:
                # 将用户添加入数据库
                insert_value = (member_id, member_name)
                connect.execute('''
                                INSERT INTO 
                                USERS(PERMISSION,ATTITUDE,GOLD,QID,QQNAME) 
                                VALUES(2,0,0,?,?);
                                ''', insert_value)
        cursor.close()
        connect.commit()
        connect.close()


# 接收指令进行刷新
@command_handler.handle()
async def refresh_user_database(bot: Bot, event: Event, state: T_State):
    # 连接数据库
    connect = sqlite3.connect(".\\Bot_data\\SQLite\\Users.db")
    # 创建游标
    cursor = connect.cursor()
    # 权限审查
    caller = event.user_id
    caller = (caller,)
    cursor.execute("SELECT COUNT(*) FROM USERS WHERE QID=(?);", caller)
    # 检查是否在数据库中
    for c in cursor:
        if c[0] == 0:
            return
        else:
            # 检查是否满足权限
            cursor.execute("SELECT PERMISSION FROM USERS WHERE QID=(?)", caller)
            for c in cursor:
                if not c[0] == 0:
                    return
    # 群组用户更新 群更新
    # 遍历群组
    groups = await bot.call_api("get_group_list")
    # groups为群组列表
    for group in groups:
        # group_id 群号
        group_id = group["group_id"]
        # group_name 群名
        group_name = group["group_name"]
        group_id_tuple = (group_id,)
        # 群更新
        # 查找数据库中是否存在该群
        cursor.execute("SELECT COUNT(*) FROM GROUPS WHERE GROUPID=(?)",group_id_tuple)
        for c in cursor:
            if c[0] == 0:
                insert_value = (group_id, group_name)
                cursor.execute('''
                                INSERT INTO
                                GROUPS(GROUPID,PERMISSION,GROUPNAME)
                                VALUES (?,1,?)
                                ''', insert_value)

        # 群用户更新
        # group_member 群成员列表
        group_members = await bot.call_api("get_group_member_list", **{"group_id": group_id})
        for group_member in group_members:
            # member_id 群成员QQ号
            member_id = group_member["user_id"]
            # 将member_id放入元组中进行数据传入
            member_id_tuple = (member_id,)
            # member_name 群成员QQ名
            member_name = group_member["nickname"]
            # 查找数据库中是否存在该成员
            cursor.execute("SELECT COUNT(*) FROM USERS WHERE QID=(?);", member_id_tuple)
            for c in cursor:
                if c[0] == 0:
                    # 避免SQL注入攻击，使用？来代替字符串替换
                    insert_value = (member_id, member_name)
                    connect.execute('''
                                    INSERT INTO 
                                    USERS(PERMISSION,ATTITUDE,GOLD,QID,QQNAME) 
                                    VALUES(2,0,0,?,?);
                                    ''', insert_value)

    # 好友用户更新 api返回json数组 详见go—cqhttp的文档
    friends = await bot.call_api("get_friend_list")
    for friend in friends:
        # 好友QQ
        friend_id = friend["user_id"]
        # 好友名
        friend_name = friend["nickname"]
        # 查找数据库中是否存在该成员
        cursor.execute("SELECT COUNT(*) FROM USERS WHERE QID=(?);", member_id_tuple)
        for c in cursor:
            if c[0] == 0:
                # 避免SQL注入攻击，使用？来代替字符串替换
                insert_value = (friend_id, friend_name)
                connect.execute('''
                                INSERT INTO 
                                USERS(PERMISSION,ATTITUDE,GOLD,QID,QQNAME) 
                                VALUES(2,0,0,?,?);
                                ''', insert_value)
    # 数据库保存更新
    cursor.close()
    connect.commit()
    connect.close()

# 导出数据库刷新函数
refresh = refresh_user_database
export().refresh = refresh


