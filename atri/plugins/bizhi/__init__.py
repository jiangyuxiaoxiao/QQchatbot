from PIL import Image
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from urllib.request import urlopen
import os

checksum=on_command("随机壁纸",priority=3)
@checksum.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
    groupid=event.group_id
    url = "https://api.iyk0.com/jxbz"
    myurl = urlopen(url)
    f = open('./Bot_data/IMAGE/patu.jpg',"wb")
    content = myurl.read()
    f.write(content)
    f.close()
    oldname="./Bot_data/IMAGE/patu.jpg"
    rename=oldname
    name_f=Image.open(rename)
    print(name_f.format)
    name_f.save(oldname)
    if 'JPEG' in name_f.format:
        print(oldname+'======='+rename)
    elif 'PNG' in name_f.format:
        rename=rename.replace("image","png")
        os.rename(oldname,rename)
        print(oldname+" ======> "+rename)
    

    await bot.call_api("send_msg",**{"message_type":"group","group_id":groupid,"message":"[CQ:image,file=file:///{}]".format(rename)})