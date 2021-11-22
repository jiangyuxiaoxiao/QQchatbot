from nonebot import on_message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from load_dictionary import dictionary
import random
import asyncio
# 引用字典
import sys
sys.path.append("../../")


# 注册一个事件响应器，事件类型为message.
reply = on_message(priority = 500, block=False)


@reply.handle()
async def normal_reply(bot: Bot, event: Event, state: T_State):
    msg = event.raw_message
    if msg in dictionary:
        if event.message_type == 'group':
            groupid = event.group_id
            # 单条回复类
            if not dictionary[msg]["multi_reply"]:
                sndmsg = dictionary[msg]["reply"][0]
            else:
                reply_len = len(dictionary[msg]["reply"])
                # 选择随机词条
                rand = random.randint(0, reply_len - 1)
                sndmsg = dictionary[msg]["reply"][rand]
            await bot.call_api("send_msg", **{"message_type": "group", "group_id": groupid,
                                              "message": "{}".format(sndmsg)})
        else:
            return
