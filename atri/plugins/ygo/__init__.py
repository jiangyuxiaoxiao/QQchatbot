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
def duel_checker1():
    async def duel_checker1(bot: Bot, event: Event, state: T_State) -> bool:
        msg = event.raw_message
        if "抽卡" == msg:
            if event.message_type == "group":
                 return True
    return Rule(duel_checker1)

# value
flag = 0
imgType_list = {'jpg','bmp','png','jpeg','rgb','tif'}
filelist = []


folder = ".\\Bot_data\\card"
# 随机抽卡
def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname


# handler
get_card = on_message(rule=duel_checker1(),block=False,priority=250)
@get_card.handle()
async def get_card(bot: Bot, event: Event, state: T_State):
    if event.post_type == "message":
        if event.message_type == "group":
            group_id = event.group_id
            global filelist, flag, folder, imgType_list
            if flag == 0:
                filelist = findAllFile(folder)
                filelist = list(filelist)
                flag = 1
            lenth = len(filelist)
            while 1:
                luckynum = random.randint(0, lenth - 1)
                file = filelist[luckynum]
                # 判断文件是否是图片
                if imghdr.what(file) in imgType_list:
                    print(file)
                    file = os.path.abspath(file)
                    file = urllib.request.pathname2url(file)
                    file = "file:" + file
                    msg = "[CQ:image,file={}]".format(file)
                    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
                    break
                else:
                    continue