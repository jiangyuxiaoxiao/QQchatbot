from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import urllib
import urllib.request



#注册一个事件响应器，事件类型为command，
joke=on_command("随机笑话",priority=21)

@joke.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
    groupid=event.group_id
    print(event.message)
    url = 'https://api.iyk0.com/xh'
    a_result = urllib.request.urlopen(url).read()
    print(a_result.decode('utf-8'))
    await bot.call_api("send_msg",**{"message_type":"group","group_id":groupid,"message":a_result.decode('utf-8')})
