from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import json
import urllib.request
from urllib.parse import urlencode

# 注册一个事件响应器，事件类型为command，
decoder = on_command("求反密", priority=1)


@decoder.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
    groupid = event.group_id
    msg = event.get_message
    data = msg()  # command后面的玩意儿
    url = 'https://api.iyk0.com/md5/dec?'
    params = {
        'md5': data
    }
    params = urlencode(params)

    # 1.f = urllib.request.urlopen('%s%s' % (url,params))
    # 2.nowapi_call = f.read()
    # 3.a_result = json.loads(nowapi_call)

    a_result = json.loads(urllib.request.urlopen('%s%s' % (url, params)).read())
    if a_result['code'] == 200:
        await bot.call_api("send_group_msg", **{"group_id": groupid, "message": "求反密成功！得到的结果是： " + a_result['text']})
    elif a_result['code'] == 202:
        print(a_result['code'])

        await bot.call_api("send_group_msg", **{"group_id": groupid, "message": "抱歉，解密失败！请稍后再试"})
