from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import json
import urllib.request
from urllib.parse import urlencode

transf = on_command("翻译", priority=50,block=True)


@transf.handle()
async def transform(bot: Bot, event: Event, state: T_State):
    group_id = event.group_id
    message = event.raw_message
    message = message.replace("翻译", "")
    message = message.replace("#", "")
    message = message.replace("/", "")
    STR_=message
    prama = {
        'text': STR_
    }
    url = 'https://api.vvhan.com/api/fy?'
    params = urlencode(prama)
    f = urllib.request.urlopen('%s%s' % (url, params))
    nowapi_call = f.read()
    a_result = json.loads(nowapi_call)
    msg = a_result['data']['fanyi']
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})


# @transf.got('city')
# async def netdisk_out(bot: Bot, event: Event, state: T_State):
#     groupid = event.group_id
#     STR_ = state["city"]
#     print(STR_)
#     prama = {
#         'text': STR_
#     }
#     url = 'https://api.vvhan.com/api/fy?'
#     params = urlencode(prama)
#     f = urllib.request.urlopen('%s%s' % (url, params))
#     nowapi_call = f.read()
#     a_result = json.loads(nowapi_call)
#     msg = a_result['data']['fanyi']
#     await bot.call_api("send_group_msg", **{"group_id": groupid, "message": msg})
