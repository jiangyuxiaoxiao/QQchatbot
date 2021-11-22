# -*- coding:utf-8 -*-
import sqlite3
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event


# 指令处理
command_handler = on_command("网盘资源", priority=250, block=True)
search_handler = on_command("网盘检索", priority=250, block=True)

@command_handler.handle()
async def netdisk_out_menu(bot: Bot, event: Event, state: T_State):
    connect = sqlite3.connect(".\\Bot_data\\SQLite\\BaiduCloudDisk.db")
    # 创建游标
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM BAIDU;")

    # 开始处理群消息指令
    if event.message_type == "group":
        # 群号
        group_id = event.group_id
        # 搜索到的资源条数
        listlen = len(list(cursor))
        if not listlen:
            msg = "没有查询到相关资源！"
            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
        else:
            cursor.execute('''
                            SELECT * 
                            FROM BAIDU
                            ORDER BY ID;''')
            msg = "网盘资源菜单如下："
            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
            # 逐页发送 避免超过长度
            i = 1
            # 总发送条数
            total_send = 0
            msg = ""
            for info in cursor:
                msg = msg + str(info[0]) + ".  "
                msg = msg + info[1] + "\n"
                # 五条五条发送
                if not i % 10:
                    msg.rstrip()
                    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
                    msg = ""
                    i = 0
                i = i + 1
                total_send = total_send + 1
                if total_send >= 50 :
                    msg = "资源总数超过50 更多信息请使用 #网盘检索"
                    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
            msg = msg + "\n请输入对应序号获取资源"
            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    cursor.close()
    connect.commit()
    connect.close()


@command_handler.got("ID")
async def netdisk_out(bot: Bot, event: Event, state: T_State):
    # 开始处理群消息指令
    if event.message_type == "group":
        group_id = event.group_id
        ID = state["ID"]
        if event.message_type == "group":
            if not ID.isdigit():
                msg = "请发送正确的数字!"
                await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
                return
            else:
                connect = sqlite3.connect(".\\Bot_data\\SQLite\\BaiduCloudDisk.db")
                # 创建游标
                cursor = connect.cursor()
                ID = int(ID)
                id_tuple = (ID,)
                cursor.execute('''
                                    SELECT * FROM BAIDU
                                    WHERE ID=(?)
                                    ORDER BY ID;''', id_tuple)
                listlen = len(list(cursor))
                # listlen 为资源条数
                if not listlen:
                    msg = "没有查询到相关资源！"
                    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
                else:
                    msg = "查询到" + str(listlen) + "条资源!"
                    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
                    cursor.execute('''
                                        SELECT * FROM BAIDU
                                        WHERE ID=(?)
                                        ORDER BY ID;''', id_tuple)
                for info in cursor:
                    msg = ""
                    msg = msg + str(info[0]) + ".  "
                    msg = msg + info[1] + ": \n"
                    msg = msg + "类型： " + info[6] + "\n"
                    msg = msg + "网盘链接： " + info[2] + "\n"
                    msg = msg + "提取码： " + info[3] + "\n"
                    msg = msg + "解压密码： " + info[4] + "\n"
                    msg = msg + "INFO： " + info[5] + "\n"
                    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
                cursor.close()
                connect.commit()
                connect.close()


# 获取搜索名字
@search_handler.handle()
async def netdisk_search_name(bot: Bot, event: Event, state: T_State):
    if event.message_type == "group":
        message=str(event.message)
        group_id = event.group_id
        if not message == "":
            state["NAME"] = message

@search_handler.got("NAME",prompt="请输入要检索的资源名！")
async def netdisk_searching(bot: Bot, event: Event, state: T_State):
    if event.message_type == "group":
        group_id = event.group_id
        connect = sqlite3.connect(".\\Bot_data\\SQLite\\BaiduCloudDisk.db")
        # 创建游标
        cursor = connect.cursor()
        NAME = state["NAME"]
        NAME = ('%'+NAME+'%',)
        #资源检索
        cursor.execute('''
                        SELECT *
                        FROM BAIDU
                        WHERE NAME LIKE (?)
                        ORDER BY ID;
                        ''', NAME)
        listlen = len(list(cursor))
        # listlen 为资源条数
        if not listlen:
            msg = "没有查询到相关资源！"
            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
        else:
            msg = "查询到" + str(listlen) + "条资源!"
            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
            cursor.execute('''
                            SELECT *
                            FROM BAIDU
                            WHERE NAME LIKE (?)
                            ORDER BY ID;
                            ''', NAME)
            total_send = 1
            for info in cursor:
                msg = str(total_send) +".  "
                msg = msg + info[1] + ": \n"
                msg = msg + "类型： " + info[6] + "\n"
                msg = msg + "网盘链接： " + info[2] + "\n"
                msg = msg + "提取码： " + info[3] + "\n"
                msg = msg + "解压密码： " + info[4] + "\n"
                msg = msg + "INFO： " + info[5] + "\n"
                total_send = total_send + 1
                await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
        cursor.close()
        connect.commit()
        connect.close()







