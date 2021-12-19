from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import GroupMessageEvent
from nonebot.rule import to_me
import os
import urllib.request
from .get_sound import text_to_sound

get_sound = on_command('语音', priority=51, rule=to_me())


@get_sound.handle()
async def text_sound(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = event.group_id
    await bot.call_api('send_msg', **{'message_type': 'group', 'group_id': group_id, 'message': '请输入文本：'})


@get_sound.got('wb')
async def text_sound(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = event.group_id
    wb = state['wb']
    filename = text_to_sound(wb)
    print(filename)
    # sound = ".\\sound\\" + wb + '.mp3'
    sound = os.path.abspath(filename)
    sound = urllib.request.pathname2url(sound)
    sound = "file:" + sound
    msg2 = "[CQ:record,file={}]".format(sound)
    print(sound)
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg2})
