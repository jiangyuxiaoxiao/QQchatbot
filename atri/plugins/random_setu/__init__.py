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

# Ruler
def setu_checker():
    async def setu_checker(bot: Bot, event: Event, state: T_State) -> bool:
        msg = event.get_message()
        msg = str(msg)
        # if msg == "来点色图" or msg == "来点涩图" or msg == "色图" or msg == "涩图" or msg == "今日盲盒" :
        if "色图" in msg or "涩图" in msg or "盲盒" in msg:
            if event.message_type == "group":
                if not event.group_id == 794284558:
                    return True
    return Rule(setu_checker)

get_setu = on_message(rule=setu_checker(),block=False,permission=SUPERUSER,priority=250)
get_setu_num = on_command("色图数量",block=False,permission=SUPERUSER,priority=250)
filelist = []
flag = 0
folder = "D:\\Data\\video\\photo"
imgType_list = {'jpg','bmp','png','jpeg','rgb','tif'}
setu_status = 0

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
            while 1 :
                luckynum = random.randint(0, lenth - 1)
                file = filelist[luckynum]
                # 判断文件是否是图片
                if imghdr.what(file) in imgType_list:
                    print(file)
                    file = urllib.request.pathname2url(file)
                    file = "file:" + file
                    msg = "[CQ:image,file={}]".format(file)
                    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
                    break
                else: continue

@get_setu_num.handle()
async def get_setu_num(bot: Bot, event: Event, state: T_State):
    if event.post_type == "message":
        if event.message_type == "group":
            group_id = event.group_id
            global filelist
            msg = str(len(filelist))
            msg = "当前色图数量：" + msg
            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
