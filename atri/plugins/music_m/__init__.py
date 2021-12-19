from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import json
import urllib.request
from urllib.parse import urlencode

from pydantic.networks import ascii_domain_regex

music = on_command("随机音乐", priority=52)
review = on_command("热评", priority=53)


@music.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
    groupid = event.group_id
    url = 'http://api.uomg.com/api/rand.music?'
    params = {
        'sort': '热歌榜',
        'format': 'json'
    }
    params = urlencode(params)
    f = urllib.request.urlopen('%s%s' % (url, params))
    nowapi_call = f.read()
    a_result = json.loads(nowapi_call)
    music_name = a_result['data']['name']
    music_artists = a_result['data']['artistsname']
    music_url = a_result['data']['url']
    str_ = 'id='
    num = music_url.find(str_)
    id_ = music_url[num + 3:]
    print(a_result['data']['url'])
    print(id)
    if 'code' in a_result and a_result['code'] == 1:
        await bot.call_api("send_msg", **{"message_type": "group", "group_id": groupid,
                                          "message": '欢迎收听来自 {} 的歌曲: {}'.format(music_artists, music_name)})
        await bot.call_api("send_msg", **{'message_type': "group", "group_id": groupid,
                                          "message": '[CQ:music,type=163,id={}]'.format(id_)})
    else:
        await bot.call_api("send_msg", **{'message_type': "group", "group_id": groupid,
                                          "message": '网络繁忙，请稍后再试'})
    music.finish()


@review.handle()
async def review(bot: Bot, event: Event, state: T_State):
    groupid = event.group_id
    url = 'https://api.uomg.com/api/comments.163?'
    global mid_
    params={
        'format':'json'
    }
    params = urlencode(params)
    f = urllib.request.urlopen('%s%s' % (url, params))
    nowapi_call = f.read()
    a_result = json.loads(nowapi_call)
    if 'code' in a_result and a_result['code']==1:
        nickname = a_result['data']['nickname']
        content = a_result['data']['content']
        await bot.call_api('send_msg', **{'message_type': "group", "group_id": groupid,
                                          "message": nickname+'说:\"'+content+'\"'})
