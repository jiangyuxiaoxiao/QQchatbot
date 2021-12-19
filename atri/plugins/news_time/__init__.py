from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import json
import urllib.request
from urllib.parse import urlencode
from nonebot.adapters.cqhttp import MessageSegment
from atri.plugins.pillow_trans import image_call                 

music = on_command("百度热搜",priority=3)
@music.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
    groupid=event.group_id
    url = 'https://api.iyk0.com/bdr/'
    msg=event.get_message
    data = msg()
    f = urllib.request.urlopen(url)
    nowapi_call = f.read()
    a_result = json.loads(nowapi_call)
    print(type(a_result))
    if 'code' in a_result:
        #if a_result['sum']>10:
         #   a_sum = 10
        a_sum = 10
        b_sum = 1
        if a_result['data'][0]['title']:
            sendmessage='{}.'.format(b_sum)+a_result['data'][0]['title']+'\n'
            while b_sum != a_sum:
                #sendmessage_a='[CQ:image,file={}]'.format(a_result["data"][b_sum]['image'])
                print(b_sum)
                sendmessage=sendmessage+'{}.'.format(b_sum+1)+a_result['data'][b_sum]['title']+'\n'
                #sendmessage_c=a_result['data'][b_sum]['url']
                #sendmessage = sendmessage_a+sendmessage_b+sendmessage_c
                b_sum = b_sum + 1
            image_call(15,a_sum,sendmessage)
            sndmsg="./Bot_data/Image/news.png"
            await bot.call_api("send_msg",**{"message_type":"group","group_id":groupid,"message":"[CQ:image,file=file:///{}]".format(sndmsg)})
            #b_sum = b_sum + 1