from nonebot import on_notice, on_command
from nonebot.typing import T_State
import json
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event, GroupDecreaseNoticeEvent, GroupIncreaseNoticeEvent, Message

indexfile = ".\\Bot_data\\Welcome\\welcome.json"

welcom = on_notice()

change_wel_word = on_command('修改欢迎语', priority=55, block=True, rule=to_me())
change_lev_word = on_command('修改离别语', priority=56, block=True, rule=to_me())


@welcom.handle()
async def wel(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):
    with open(indexfile, encoding="utf-8") as fp:
        index = json.load(fp)
        word_in = index["in"]
    user = event.get_user_id()
    at_ = '[CQ:at,qq={}]'.format(user)
    msg = at_ + word_in
    msg = Message(msg)
    await welcom.finish(message=msg)


@welcom.handle()
async def wel(bot: Bot, event: GroupDecreaseNoticeEvent, state: T_State):
    with open(indexfile, encoding="utf-8") as fp:
        index = json.load(fp)
        word_out = index["out"]
    user = event.get_user_id()
    at_ = '[CQ:at,qq={}]'.format(user)
    msg = at_ + word_out
    msg = Message(msg)
    await welcom.finish(message=msg)


@change_wel_word.handle()
async def cha_wel_word(bot: Bot, event: Event, state: T_State):
    group_id = event.group_id
    user_id = event.user_id
    user = await bot.call_api("get_group_member_info", **{"group_id": group_id, "user_id": user_id})
    if user["role"] == 'member':
        msg = "只有群主或者管理员能修改！"
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
        return
    msg = "请输入欢迎语："
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})


@change_wel_word.got("wel_word")
async def cha_welword(bot: Bot, event: Event, state: T_State):
    wel_word = state["wel_word"]
    group_id = event.group_id
    dict = {}
    with open(indexfile, encoding="utf-8") as fp:
        index = json.load(fp)
        dict = index
    fp.close()
    dict["in"] = wel_word
    with open(indexfile, 'w', encoding="utf-8") as r:
        # 定义为写模式，名称定义为r

        json.dump(dict, r)
        # 将dict写入名称为r的文件中

    r.close()
    msg = "欢迎语已经修改为：\n" + wel_word + "\n修改成功！"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})


@change_lev_word.handle()
async def cha_lev_word(bot: Bot, event: Event, state: T_State):
    group_id = event.group_id
    user_id = event.user_id
    user = await bot.call_api("get_group_member_info", **{"group_id": group_id, "user_id": user_id})
    if user["role"] == 'member':
        msg = "只有群主或者管理员能修改！"
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
        return
    msg = "请输入离别语："
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})


@change_lev_word.got("wel_word")
async def cha_levword(bot: Bot, event: Event, state: T_State):
    wel_word = state["wel_word"]
    group_id = event.group_id
    dict = {}
    with open(indexfile, encoding="utf-8") as fp:
        index = json.load(fp)
        dict = index
    fp.close()
    dict["out"] = wel_word
    with open(indexfile, 'w', encoding="utf-8") as r:
        # 定义为写模式，名称定义为r

        json.dump(dict, r)
        # 将dict写入名称为r的文件中

    r.close()
    msg = "离别语已经修改为：\n" + wel_word + "\n修改成功！"
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
