# -*- encoding:utf-8 -*-
import json
import sqlite3
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from .register_zoom import *
from .get_pat import *
from .show_my_pet import *
from .is_player import *
from .fight_system import fight
from .show_bag import show_bagg
from .buy_ import *

player = ''
get_id_list = on_command('宠物乐园玩家', priority=250, permission=SUPERUSER)
put_menu = on_command('宠物乐园', priority=250, block=True)
create_id = on_command('注册', priority=250)
get_a_pat = on_command('获取宠物', priority=250)
my_pet = on_command('我的宠物', priority=250, block=True)
fightt = on_command('战斗', priority=250, block=True)
bag = on_command('宠物背包', priority=250, block=True)
store__ii = on_command('宠物商城', priority=250, block=True)
use_invitation = on_command('使用邀请函',priority=250,block=True)

db = './Bot_data/My_zoom/common.db'


@get_id_list.handle()
async def get_id_put(bot: Bot, event: Event, state: T_State):
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    cursor.execute('select * from user;')
    group_id = event.group_id
    user_num = 1
    msg = ""
    for info in cursor:

        for mes in info:
            msg = msg + str(mes) + ' '
        if not user_num % 10:
            user_num = 1
            await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})
            msg = ""
        else:
            msg = msg + '\n'
    await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})
    print(msg)
    cursor.close()
    connect.commit()
    connect.close()


@create_id.handle()
async def create_user(bot: Bot, event: Event, state: T_State):
    if event.sub_type != 'normal':
        return
    user_id = str(event.user_id)
    name = event.sender.nickname
    msg = register(id=user_id, name=name)

    group_id = event.group_id
    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})


@put_menu.handle()
async def outputmenu_(bot: Bot, event: Event, state: T_State):
    if event.sub_type != 'normal':
        return
    global player
    player = str(event.sender.nickname)

    group_id = event.group_id
    menu_msg = f'''--欢迎来到宠物乐园--
    {player}欢迎回家。
    具体功能有：
    获取宠物
    我的宠物
    战斗
    宠物背包
    宠物商城
    使用邀请函
    '''
    await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': menu_msg})


@get_a_pat.handle()
async def get_apat(bot: Bot, event: Event, state: T_State):
    if event.sub_type != 'normal':
        return
    user_id = str(event.user_id)
    group_id = event.group_id
    msg = get_a_new_pat(id=user_id)
    await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})


@my_pet.handle()
async def mypets(bot: Bot, event: Event, state: T_State):
    if event.sub_type != 'normal':
        return
    user_id = str(event.user_id)
    group_id = event.group_id
    msgs = show_pet(user_id=user_id)
    for msg in msgs:
        await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})


@fightt.handle()
async def fight_s(bot: Bot, event: Event, state: T_State):
    if event.sub_type != 'normal':
        return
    user_id = str(event.user_id)
    group_id = event.group_id
    if not isplayer(user_id=user_id):
        msg = "你还未加入宠物乐园，请先注册！"
        await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})
        return
    else:
        msg = "请@出你想发起挑战的对象。"
        # # 外部变量player用来保存挑战者
        # global player
        # player = user_id
        await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})


@fightt.got('fight_to')
async def fight_t(bot: Bot, event: Event, state: T_State):
    if event.sub_type != 'normal':
        return
    user_id = str(event.user_id)
    # #当前发送消息的玩家不是刚才申请战斗的那个
    # if user_id != player:
    #     return
    group_id = event.group_id
    fight_to = state['fight_to']
    fight_to = fight_to.replace(" ", "")
    fight_to = fight_to[10:-1]
    print(fight_to)
    try:
        print(int(fight_to))
    except:
        print('error')
        msg = '请只是@你要挑战的对象！'
        await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})
        return

    if fight_to == str(event.user_id):
        msg = '不要和自己打架！！！！！'
        await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})
        return
    if not isplayer(user_id=fight_to):
        msg = "对战失败！\n你选择的对象还不是宠物乐园的小伙伴。\n邀请他注册加入吧！"
        await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})
        return
    else:
        player1 = str(event.user_id)
        # print(fight_to)
        player2 = fight_to
        message = fight(player1=player1, player2=player2)
        message_2 = []
        msg = ""
        num = 1
        for msg_2 in message:
            msg = msg + msg_2 + '\n'
            num += 1
            if not num % 15:
                message_2.append(msg)
                msg = ""
        if msg:
            message_2.append(msg)
        for msg_1 in message_2:
            await bot.call_api("send_group_msg", **{'group_id': group_id, "message": msg_1})


@bag.handle()
async def get_bag(bot: Bot, event: Event, state: T_State):
    if event.sub_type != 'normal':
        return
    user_id = str(event.user_id)
    group_id = event.group_id
    if not isplayer(user_id=user_id):
        msg = "你还未加入宠物乐园，请先注册！"
        await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})
        return

    msg = show_bagg(user_id=user_id)
    await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})
    return


@store__ii.handle()
async def store(bot: Bot, event: Event, state: T_State):
    if event.sub_type != 'normal':
        return
    user_id = str(event.user_id)
    group_id = event.group_id
    if not isplayer(user_id=user_id):
        msg = "你还未加入宠物乐园，请先注册！"
        await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})
        return

    filename = "./Bot_data/My_zoom/store.json"

    with open(filename, encoding="UTF-8") as fp:
        shop = json.load(fp)
        shops = shop["shop"]

    msg1 = "🎊🎊🎉欢迎购买🎉🎊🎊\n"
    msg = ""
    num = 0;
    for shop in shops:
        num+=1
        msg = msg + str(num) + " " + shop["name"] + "价格:" + str(shop["price"]) + "💰\n"
    await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})
    msg = "请问你想买什么？"
    await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})


@store__ii.got('buy')
async def shopping(bot: Bot, event: Event, state: T_State):
    user_id = str(event.user_id)
    group_id = event.group_id
    filename = "./Bot_data/My_zoom/store.json"
    with open(filename, encoding="UTF-8") as fp:
        shop = json.load(fp)
        shops = shop["shop"]

    buy = int(state['buy'])
    if buy <= 0 or buy > len(shops):
        msg = "请正确输入商品号码！"
        await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})
        return

    coins = get_coin(user_id=user_id)
    print(coins,shops[buy - 1]["price"])
    if coins < shops[buy - 1]["price"]:
        msg = "哦~~金币不够哦~~~"
        await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})
        return

    x=buyitems(user_id=user_id,buy=buy)
    print(x)
    try:
        x=buyitems(user_id=user_id, buy=buy)
        if x:
            msg="购买成功！"

        else:
            msg="购买失败！"

    except:
        msg="购买失败！"
    await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})
    return


@use_invitation.handle()
async def use_inviation(bot:Bot,event:Event,state:T_State):
    if event.sub_type != 'normal':
        return
    user_id = str(event.user_id)
    group_id = event.group_id
    if not isplayer(user_id=user_id):
        msg = "你还未加入宠物乐园，请先注册！"
        await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})
        return
    msg=use_invi(user_id=user_id)
    print(msg)
    await bot.call_api("send_group_msg", **{'group_id': group_id, 'message': msg})