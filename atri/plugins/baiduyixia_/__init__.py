from nonebot.adapters.cqhttp import Bot, Event
import requests
from nonebot.rule import Rule
from nonebot import on_command, on_message
from nonebot.typing import T_State
from .Baidu_Rule import baiduyixia_rulee
import string

getmusic = on_command('回家', priority=57)


baidu_yixia = on_message(rule=baiduyixia_rulee(), priority=58)


@getmusic.handle()
async def getmusic(bot: Bot, event: Event):
    group_id = event.group_id
    title = '这是托利亚的家'
    content = '托利亚有一个温馨的小家！'
    image = 'https://www.xn--jlq249bliy.com/wp-content/uploads/2021/10/Atri3.jpg'
    await bot.call_api('send_msg', **{'message_type': 'group', 'group_id': group_id,
                                      'message': f'[CQ:share,url=https://www.xn--jlq249bliy.com,title={title},'
                                                 f'content={content},image={image}]'})


@baidu_yixia.handle()
async def baiduyixia_(bot: Bot, event: Event, state: T_State):
    message = event.raw_message
    if '百度' in message:
        message = message.replace("百度", "")
    if '查一下' in message:
        message = message.replace("查一下", "")
    group_id = event.group_id
    print(message)
    title="帮你找到答案啦！"
    image = 'https://www.xn--jlq249bliy.com/wp-content/uploads/2021/10/Atri3.jpg'
    url = "https://baike.baidu.com/item/" + message
    await bot.call_api('send_group_msg', **{'group_id': group_id,
                                            'message': f'[CQ:share,url={url},title={title},'
                                                       f'content={message},image={image}]'})
