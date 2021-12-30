import json
import urllib.request

import nonebot
from nonebot import require,get_driver
from nonebot.permission import SUPERUSER
from nonebot.plugin import require
from nonebot.typing import T_State
from .pillow_trans import image_call 

scheduler_baidu_resou = require("nonebot_plugin_apscheduler").scheduler

@scheduler_baidu_resou.scheduled_job("cron", hour = "*/1")#定期发送时间

async def baidu_resou():
    bot = nonebot.get_bot()
    groups = await bot.call_api('get_group_list')
    print(groups)
    url = 'https://api.iyk0.com/bdr/'
    f = urllib.request.urlopen(url)
    nowapi_call = f.read()
    a_result = json.loads(nowapi_call)
    print(type(a_result))
    if 'code' in a_result:
        a_sum = 30 #获取条数 最多30
        b_sum = 1
        if a_result['data'][0]['title']:
            sendmessage='{}.'.format(b_sum)+a_result['data'][0]['title']+'\n'
            while b_sum != a_sum:              
                sendmessage=sendmessage+'{}.'.format(b_sum+1)+a_result['data'][b_sum]['title']+'\n'                
                b_sum = b_sum + 1
            image_call(15,a_sum,sendmessage)
            sndmsg="./Bot_data/Image/news.png"
            for group in groups:
                print(group['group_id'])
                #if group['group_id'] == 994387105:
                #    print("success!")
                groupid = group['group_id']
                    #要发送的群 群号
                await bot.call_api("send_group_msg",**{"group_id":groupid,"message":"[CQ:image,file=file:///{}]".format(sndmsg)})
                #else:
                #    print("failed!")