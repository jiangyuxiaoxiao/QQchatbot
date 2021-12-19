from nonebot import require, get_driver
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
import nonebot
from .get_news import news_
import json

scheduler_read_world = require("nonebot_plugin_apscheduler").scheduler

msg = news_()

indexfile = ".\\Bot_data\\Read_Time\\time.json"
with open(indexfile, encoding="utf-8") as fp:
    index = json.load(fp)
    time = index["time"]
    hour = time["hour"]
    minute = time["minute"]


@scheduler_read_world.scheduled_job("cron", hour=hour, minute=minute)
async def read_world():
    bot = nonebot.get_bot()
    groups = await bot.call_api('get_group_list')
    print(groups)
    global msg
    for group in groups:
        groupid = group['group_id']
        await bot.call_api('send_group_msg', **{"group_id": groupid, 'message': msg})

