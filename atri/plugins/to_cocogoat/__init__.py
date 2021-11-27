# -*- coding:utf-8 -*-
import nonebot
from nonebot import require
from nonebot.rule import Rule
from nonebot.rule import to_me, keyword
from nonebot import on_message, on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import SUPERUSER
import time
import random
import asyncio

# scheduler
scheduler = require("nonebot_plugin_apscheduler").scheduler
# debug 用户库刷新调用
refresh = require("database_management").refresh
# Ruler
def coco_checker1():
    async def inner_checker(bot: Bot, event: Event, state: T_State) -> bool:
        msg = event.get_message()
        msg = str(msg)
        if "修仙结束" in msg:
            if "168934818" in msg:
                return True
    return Rule(inner_checker)

def coco_checker2():
    async def inner_checker(bot: Bot, event: Event, state: T_State) -> bool:
        msg = event.get_message()
        msg = str(msg)
        if "捞瓶五连" in msg:
            return True
    return Rule(inner_checker)

rule2 = keyword("查看角色")
# checker
has_corrupt = 0
# Handler
cocogoat_end_xiuxian = on_message(rule=coco_checker1(), priority=200, block=False)
cocogoat_command1 = on_message(rule=rule2, priority=200, block=False, permission=SUPERUSER)
cocogoat_auto_fight = on_command("亚托莉俯冲轰炸机", priority=300, block=False, permission=SUPERUSER)
# cocogoat_auto_task = on_command("亚托莉自动巡航轰炸机", priority=300, block=False, permission=SUPERUSER)
cocogoat_forbid_fighting = on_message(rule=to_me(), priority=1, block=False)
cocogoat_find_corruption = on_message(priority=300, block=False)
cocogoat_defend = on_message(priority=300, block=False)
cocogoat_daily = on_command("托莉日常",priority=400, block=False, permission=SUPERUSER)
cocogoat_tritri = on_command("托莉剑法",priority=500,block=False,permission=SUPERUSER)
# cocogoat_master_repeat = on_message(permission=SUPERUSER,priority=450,block=False)
cocogoat_get_bottle = on_message(rule=coco_checker2(),block=False,priority=250)

@scheduler.scheduled_job('cron',hour = '*/6')
async def scheduled_xiuxian():
    bot = nonebot.get_bot()
    group_id = 974539308
    msg = "开始修仙"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})


@cocogoat_end_xiuxian.handle()
async def reply_xiuxian(bot: Bot, event: Event, state: T_State):
    group_id = 974539308
    msg = "开始修仙"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})


@cocogoat_command1.handle()
async def reply_check(bot: Bot, event: Event, state: T_State):
    group_id = 974539308
    msg = "查看角色"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})


@cocogoat_auto_fight.handle()
async def func_atri_bomb(bot: Bot, event: Event, state: T_State):
    if event.message_type == "group":
        message = str(event.message)
        group_id = event.group_id
        if not message == "":
            state["QID"] = message


@cocogoat_auto_fight.got("QID")
async def func_atri_bomb_activate(bot:Bot, event:Event, state: T_State):
    group_id = event.group_id
    QID = state["QID"]
    QID = QID.replace("[CQ:at,qq=","")
    QID = QID.replace("]","")
    QID = int(QID)
    msg = " アトリは、高性能ですから!"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    file = "file:///C:/Users/65416/Desktop/atri_iron_fist.jpg"
    msg = "吃我组合鱼雷拳！[CQ:image,file={}]".format(file)
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    msg = "对战[CQ:at,qq={}]".format(QID)
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    msg = "攻击[CQ:at,qq={}]".format(QID)
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    msg = "逃跑"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    await asyncio.sleep(0.25)
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    await refresh(bot,event,state)


@cocogoat_forbid_fighting.handle()
async def run_run_run(bot: Bot, event: Event, state: T_State):
    if event.post_type == "message":
        if event.message_type == "group":
            message = str(event.message)
            if message == "对战" or message == "攻击" or message == "使用技能" or message == "使用大招":
                if event.group_id == 974539308:
                    group_id = 974539308
                    msg = "逃跑"
                    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
                    for i in range(1,3):
                        time.sleep(0.2)
                        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
                    msg = "哼哼，晚上可不要睡得太死哟！"
                    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})

'''
@scheduler.scheduled_job("cron", hour="03", minute="00")
async def cocogoat_assasin():
    global has_corrupt
    bot = nonebot.get_bot()
    group_id = 974539308
    group_list = await bot.call_api("get_group_member_list", **{"group_id": group_id})
    member_num = len(group_list)
    lucky_guy = random.randint(0,member_num-1)
    QID = group_list[lucky_guy]["user_id"]
    QNAME = group_list[lucky_guy]["nickname"]
    breakflag = 0
    has_corrupt = 0
    msg = "自动任务已展开，锁定幸运观众：{}".format(QNAME)
    msg = msg + "\n轰炸机已抵达"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    while 1:
        msg = "对战[CQ:at,qq={}]".format(QID)
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
        msg = "攻击[CQ:at,qq={}]".format(QID)
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
        msg = "逃跑"
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
        await asyncio.sleep(0.25)
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
        await asyncio.sleep(5)
        if has_corrupt == 1:
            has_corrupt = 0
            breakflag = 0
            lucky_guy = random.randint(0, member_num - 1)
            QID = group_list[lucky_guy]["user_id"]
            QNAME = group_list[lucky_guy]["nickname"]
            msg = "目标暂时无法接听，已更换幸运观众：{}，正在重新锁定".format(QNAME)
            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
            await asyncio.sleep(300)
            continue
        await asyncio.sleep(650)
        breakflag = breakflag + 1
        msg = "已成功执行{}/10次任务！".format(breakflag)
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
        if breakflag == 10:
            break
'''


@cocogoat_find_corruption.handle()
async def find_corruption(bot:Bot, event:Event, state: T_State):
    global has_corrupt
    if event.post_type == "message":
        if event.message_type == "group":
            if event.group_id == 974539308:
                if event.user_id == 3337549065:
                    msg = event.message
                    msg = str(msg)
                    if msg == "对方暂时没有行动能力哦":
                        has_corrupt = 1
                    if msg == "你要对无辜的路人下手吗？真可耻！":
                        has_corrupt = 1
                    if msg == "鞭尸是不道德的！":
                        has_corrupt = 1

'''
@cocogoat_auto_task.handle()
async def auto_task(bot:Bot, event:Event, state: T_State):
    await cocogoat_assasin()
'''

@cocogoat_defend.handle()
async def defend(bot:Bot, event:Event, state: T_State):
    if event.post_type == "message":
        if event.message_type == "group":
            if event.group_id == 974539308:
                if event.user_id == 123456789:
                    group_id = 974539308
                    msg = event.message
                    msg = str(msg)
                    if "搜图" in msg:
                        file = "file:///C:/Users/65416/Desktop/atri_iron_fist.jpg"
                        msg = "吃我组合鱼雷拳！[CQ:image,file={}]".format(file)
                        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
                        for i in range(1,10):
                            msg = "搜图 樱井宁宁"
                            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})

@cocogoat_daily.handle()
async def daily(bot:Bot, event:Event, state: T_State):
    group_id = 974539308
    msg = "签到"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    msg = "投食"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    msg = "查看"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    msg = "查看角色"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    for i in range(1,60):
        msg = "？"
        await asyncio.sleep(120)
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    msg = "好感度上限"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})


@scheduler.scheduled_job('cron',hour = '03', minute="00")
async def scheduled_job():
    group_id = 974539308
    bot = nonebot.get_bot()
    msg = "签到"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    msg = "投食"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    msg = "查看"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    msg = "查看角色"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    for i in range(1,120):
        msg = "？"
        await asyncio.sleep(20)
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    msg = "好感度上限"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})


@cocogoat_tritri.handle()
async def func_atri_bomb(bot: Bot, event: Event, state: T_State):
    if event.message_type == "group":
        message = str(event.message)
        group_id = event.group_id
        if not message == "":
            state["QID"] = message

@cocogoat_tritri.got("QID")
async def tritri(bot:Bot, event:Event, state: T_State):
    group_id = event.group_id
    QID = state["QID"]
    QID = QID.replace("[CQ:at,qq=", "")
    QID = QID.replace("]", "")
    QID = int(QID)
    msg = " アトリは、高性能ですから!"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    file = "file:///C:/Users/65416/Desktop/atri_iron_fist.jpg"
    msg = "吃我组合鱼雷拳！[CQ:image,file={}]".format(file)
    # await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    msg = "[CQ:poke,qq={}]".format(QID)
    for i in range(1,10):
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
        await asyncio.sleep(20)

'''
@cocogoat_master_repeat.handle()
async def cocogoat_master_repeat(bot:Bot, event:Event, state: T_State):
    if event.message_type == "group":
        msg = str(event.message)
        if "蕾姆" in msg:
            msg = msg.replace("蕾姆","拉姆")
        elif "拉姆" in msg:
            msg = msg.replace("拉姆","蕾姆")
        if "www" in msg:
            msg = msg.replace("www","w w w")
        if "http" in msg:
            msg = msg.replace("http","h t t p")
        if "." in msg:
            msg = msg.replace(".","。")
        group_id = event.group_id
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
'''

@cocogoat_get_bottle.handle()
async def cocogoat_get_bottle(bot:Bot, event:Event, state: T_State):
    if event.post_type == "message":
        if event.message_type == "group":
            if event.group_id == 974539308:
                group_id = 974539308
                msg = "捞瓶子"
                for i in range(1, 6):
                    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
                    await asyncio.sleep(0.5)