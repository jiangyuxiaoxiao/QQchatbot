# -*- coding:utf-8 -*-

from nonebot.rule import to_me, keyword
from nonebot import on_message, on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import SUPERUSER
# http请求
import requests

# 调用api的url，详情可以看百度云的技术文档
request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
# 规则 ：当@亚托莉时触发
auditing = on_message(rule=to_me(),priority=230,block=False)
# 百度api的acess_token是有时间限制的，通过该函数刷新acess_token
get_access = on_command("接口获取",permission=SUPERUSER,priority=230,block=False)
# 本地存储的access_token,一般有效期为三十天
access_token = "24.b49f59c9e074b4a42894e3cdaa0e74bb.2592000.1639907878.282335-25163869"


@auditing.handle()
async def auditing(bot: Bot, event: Event, state: T_State):
    # API调用URL
    # 权限参数
    # 调用全局变量需显式声明
    global access_token
    global request_url
    # 请求报文头
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # 一定要检查消息是群消息还是私聊
    if event.message_type == "group":
        group_id = event.group_id
        user_id = event.user_id
        message = event.message
        message = str(message)
        # 调用百度api要求的格式，对于不同的api请参考不同的文档
        send_message = {"text":"{}".format(message)}
        # url生成
        request_url = request_url + "?access_token=" + access_token
        # print(request_url) 测试用
        # 调用API
        response = requests.post(request_url, data=send_message, headers=headers)
        if response:
            print(response.json())
        # API返回了一个json变量，具体格式参考文档
        response = response.json()
        if response["conclusion"] == "不合规":
            if response["data"][0]["subType"] == 5:
                message = message.replace("我","你")
                message = message.replace("亚托莉","你")
                message = message.replace("atri", "你")
                message = message.replace("ATRI", "你")
                message = message.replace("Atri", "你")
                message = "[CQ:at,qq={}]".format(user_id) + message
                await bot.call_api("send_msg",
                                   **{"message_type": "group", "group_id": group_id, "message": "{}".format(message)})
            if  response["data"][0]["subType"] == 2:
                message = "?"
                await bot.call_api("send_msg",
                                   **{"message_type": "group", "group_id": group_id, "message": "{}".format(message)})
                message = "[CQ:at,qq={}]NMSL".format(user_id)
                await bot.call_api("send_msg",
                                   **{"message_type": "group", "group_id": group_id, "message": "{}".format(message)})
                message = "傻X"
                await bot.call_api("send_msg",
                                   **{"message_type": "group", "group_id": group_id,"message": "{}".format(message)})


    if event.message_type == "private":
        return


@get_access.handle()
async def auditing(bot: Bot, event: Event, state: T_State):
    # acess_token如何获得请参考文档
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=bU33WRfrO2AMaiv7PybhXn5v&client_secret=resEmLpvhgyk0jOcKe9BCDTn5sR0bhPW'
    access_token = requests.get(host)
    if access_token:
        print(access_token.json())
