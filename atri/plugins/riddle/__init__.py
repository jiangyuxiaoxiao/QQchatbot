from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import json
import urllib.request
from urllib.parse import urlencode
import time



#注册一个事件响应器，事件类型为command，
riddle=on_command("随机谜语",priority=10)
@riddle.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
    
    groupid=event.group_id
    url = 'https://api.iyk0.com/miyu'
    
    a_result = json.loads(urllib.request.urlopen(url).read())

    await bot.call_api("send_group_msg", **{"group_id": groupid, "message": '题： ' + a_result['puzzle'] + '\n' + '类型： ' + a_result['type'] + '\n' + '提示： ' + a_result['tip'] + '\n' + '答案会在20秒后发送'})
    time.sleep(20)
    await bot.call_api("send_group_msg", **{"group_id": groupid, "message": '答案为： ' + a_result['answer']})
