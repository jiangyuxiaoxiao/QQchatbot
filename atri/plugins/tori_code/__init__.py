import os.path

import rsa
from nonebot import on_command
from nonebot import on_notice
import urllib.request
from nonebot.rule import to_me
import time
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event

encoder = on_command("托莉rsa加密",priority=100,block=True)
decoder = on_command("托莉rsa解密",priority=120,block=True)


def encode(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])


def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

@encoder.handle()
async def encoder_handle(bot: Bot, event: Event, state: T_State):
    if event.message_type == "group":
        message=str(event.message)
        group_id = event.group_id
        if not message == "":
            state["origin"] = message

@encoder.got("origin")
async def encoder_got(bot: Bot, event: Event, state: T_State):
    if event.message_type == "group":
        group_id = event.group_id
        originstring = state["origin"]
        pubkey = "./Bot_data/web/pubkey.pem"
        user_id = event.get_user_id()
        encodefile = "./Bot_data/web/{}.atri".format(user_id)
        with open(pubkey,mode="rb") as pubf:
            pubkey = pubf.read()
            pubkey = rsa.PublicKey.load_pkcs1(pubkey)
            msg = rsa.encrypt(originstring.encode('utf-8'),pubkey)
            with open(encodefile,mode="wb") as f:
                f.write(msg)
            save_as = "@"+ str(user_id) + ".txt"
            save_as =time.strftime("%Y年%m月%d日@%H点%M分%S秒", time.localtime()) + save_as
            encodefile = os.path.abspath(encodefile)
            print(encodefile)
            print(save_as)
            await bot.call_api("upload_group_file", **{"group_id": group_id, "name": save_as, "file":encodefile})
            msg = "加密文件已保存为: {}".format(save_as)
            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})


@decoder.handle()
async def decoder_handle(bot: Bot, event: Event, state: T_State):
    if event.message_type == "group":
        message=str(event.message)
        group_id = event.group_id
        if not message == "":
            state["origin"] = message


@decoder.got("origin")
async def decoder_got(bot: Bot, event: Event, state: T_State):
    if event.message_type == "group":
        group_id = event.group_id
        user_id = event.get_user_id()
        filename = state["origin"]
        privkey = "./Bot_data/web/privkey.pem"
        files = await bot.call_api("get_group_root_files",**{"group_id":group_id})
        files = files["files"]
        file_id = 0
        flag = 0
        for file in files:
            if file["file_name"] == filename:
                file_id = file["file_id"]
                busid = file["busid"]
                print(file_id)
                print(filename)
                print(busid)
                file_url = await bot.call_api("get_group_file_url",**{"group_id":group_id,"file_id":file_id,"busid":busid})
                file = await bot.call_api("download_file",**{"url":file_url})
                print(file)
                flag = 1
                break
        if flag == 0:
            msg = "托莉没有找到文件哦"
            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
            return
        with open(privkey,mode="rb") as prif:
            privkey = prif.read()
            privkey = rsa.PrivateKey.load_pkcs1(privkey)
            with open(file,mode="rb") as f:
                f = f.read()
                msg = rsa.decrypt(f,privkey)
                msg = msg.decode('utf-8')
            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
