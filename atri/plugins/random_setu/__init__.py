# -*- coding: utf-8 -*-
import os
import urllib.request
import imghdr
from nonebot import on_command,on_message
from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import SUPERUSER
import random
import json

sender_id = 261257365
sender_name = "椰羊"

class Nodes():
    nodes = []
    def __init__(self):
        self.nodes = []
        return

    def add_node(self,qid,name,content):
        node_info = {}
        node_info["type"] = "node"
        node_info["data"] = {
            "name":name,
            "uin":str(qid),
            "content":content
        }
        self.nodes.append(node_info)
        return

    def node_msg(self):
        return self.nodes

    def node_clear(self):
        self.nodes = []
        return

# Ruler
def setu_checker():
    async def setu_checker(bot: Bot, event: Event, state: T_State) -> bool:
        msg = event.raw_message
        # if msg == "来点色图" or msg == "来点涩图" or msg == "色图" or msg == "涩图" or msg == "今日盲盒" :
        if "来点涩图" in msg:
            if event.message_type == "group":
                 return True
    return Rule(setu_checker)


get_setu = on_message(rule=setu_checker(),block=False,priority=250)
get_setu_num = on_command("色图数量",block=False,permission=SUPERUSER,priority=250)
set_name = on_command("色批指定",block=False,priority=250)


filelist = []
flag = 0
folder = "D:/Data/video/photo"
imgType_list = {'jpg','bmp','png','jpeg','rgb','tif'}
setu_status = 1

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname


@get_setu.handle()
async def get_setu(bot: Bot, event: Event, state: T_State):
    global setu_status
    if setu_status == 0:
        return
    if event.post_type == "message":
        if event.message_type == "group":
            group_id = event.group_id
            global filelist,flag,folder,imgType_list
            if flag == 0:
                filelist = findAllFile(folder)
                filelist = list(filelist)
                '''
                for i in filelist:
                    print(i)
                '''
                flag = 1
            lenth = len(filelist)
            count = 0
            ### 转发
            nodemsg = Nodes()
            # print(len(nodemsg.node_msg()))
            global sender_name, sender_id
            ### 转发

            while 1 :
                luckynum = random.randint(0, lenth - 1)
                file = filelist[luckynum]
                # 判断文件是否是图片
                if imghdr.what(file) in imgType_list:
                    print(file)
                    file = urllib.request.pathname2url(file)
                    file = "file:" + file
                    msg = "[CQ:image,file={}]".format(file)
                    count = count + 1
                    nodemsg.add_node(sender_id, sender_name,msg)
                    if count == 10:
                        break
                else: continue

            # print(nodemsg.node_msg())
            msg = "空投涩图中"
            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
            await bot.call_api("send_group_forward_msg",**{"group_id":group_id,"messages":nodemsg.node_msg()})


@get_setu_num.handle()
async def get_setu_num(bot: Bot, event: Event, state: T_State):
    if event.post_type == "message":
        if event.message_type == "group":
            group_id = event.group_id
            global filelist
            msg = str(len(filelist))
            msg = "当前色图数量：" + msg
            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})


@set_name.handle()
async def set_name_handler(bot: Bot, event: Event, state: T_State):
    if event.message_type == "group":
        message = str(event.message)
        group_id = event.group_id
        if not message == "":
            state["QID"] = message

@set_name.got("QID")
async def tritri(bot:Bot, event:Event, state: T_State):
    group_id = event.group_id
    QID = state["QID"]
    QID = QID.replace("[CQ:at,qq=", "")
    QID = QID.replace("]", "")
    QID = int(QID)
    global sender_name,sender_id
    sender_id = QID
    sender_name = await bot.call_api("get_group_member_info",**{"group_id":group_id,"user_id":QID})
    sender_name = sender_name["nickname"]
    msg = "指定成功，今天的老色批是：{}".format(sender_name)
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
