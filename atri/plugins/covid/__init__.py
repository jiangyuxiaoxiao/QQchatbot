from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import json
import urllib.request
from urllib.parse import urlencode

# 注册一个事件响应器，事件类型为command，
encoder = on_command("疫情情况", priority=51,block=False)


@encoder.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
    groupid = event.group_id
    msg = event.get_message
    data = msg()  # command后面的玩意儿
    url = 'https://api.iyk0.com/yq/?'
    params = {
        'msg': data
    }
    params = urlencode(params)

    # 1.f = urllib.request.urlopen('%s%s' % (url,params))
    # 2.nowapi_call = f.read()
    # 3.a_result = json.loads(nowapi_call)

    a_result = json.loads(urllib.request.urlopen('%s%s' % (url, params)).read())
    if a_result['code'] == 200:

        await bot.call_api("send_group_msg", **{"group_id": groupid, "message": "查询地区: " + a_result["查询地区"] + '\n' + "目前确诊: " + a_result["目前确诊"] + '\n' + "死亡人数: " + a_result["死亡人数"] + '\n' + "治愈人数: " + a_result["治愈人数"] + '\n' +
    "新增确诊: " + a_result["新增确诊"] + '\n' + "现存确诊: " + a_result["现存确诊"] + '\n' + "现存无症状: " + a_result["现存无症状"] + '\n' + "time: " + a_result["time"]
    })
    elif a_result['code'] == 202:
        print(a_result['code'])
        await bot.call_api("send_group_msg", **{"group_id": groupid, "message": "抱歉，查找失败！请稍后再试！！！"})
