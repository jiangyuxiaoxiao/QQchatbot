from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import random

waifu=on_command("获取老婆",priority=1)

@waifu.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
    randnum=random.randint(5000,50000)
    groupid=event.group_id
    sndmsg="https://www.thiswaifudoesnotexist.net/example-"+str(randnum)+".jpg"
    await bot.call_api("send_msg",**{"message_type":"group","group_id":groupid,"message":"[CQ:image,file={}]".format(sndmsg)})