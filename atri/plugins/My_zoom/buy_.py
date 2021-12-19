import sqlite3
import json
import random
from .get_pat import *

commondb = ".\\Bot_data\\My_zoom\\common.db"
indexfile = ".\\Bot_data\\My_zoom\\bag.json"
indexfile1='.\\Bot_data\\My_zoom\\get_pat.json'
indexfile2 = ".\\Bot_data\\My_zoom\\store.json"

#获取玩家的金币数
def get_coin(user_id)->int:

    #连接数据库
    connect=sqlite3.connect(commondb)
    #创建游标
    cursor=connect.cursor()
    #查询数据
    cursor.execute("select coins from bag where id={}".format(user_id))
    coins=cursor.fetchall()
    #cursor.fetchall得到的是一个包含元组的列表
    coins=coins[0][0]

    return coins

def use_invi(user_id):
    # 连接数据库
    connect = sqlite3.connect(commondb)
    # 创建游标
    cursor = connect.cursor()
    # 查询数据
    cursor.execute("select invitation from bag where id={}".format(user_id))
    invitation = cursor.fetchall()
    # cursor.fetchall得到的是一个包含元组的列表
    invitation = invitation[0][0]

    if invitation<=0:
        return "你的邀请函不够哦！去宠物商城看看吧！"

    else:
        invitation-=1;
        cursor.execute(f"update bag set invitation={invitation} where id={user_id}")
        cursor.execute(f"update user set last_get=0 where id={user_id}")
        connect.commit()
        cursor.close()
        connect.close()
        msg=get_a_new_pat(user_id)
        return msg


def buyitems(user_id,buy):
    #买的是邀请函
    if buy == 4:
        connect = sqlite3.connect(commondb)
        cursor = connect.cursor()
        now_coin=get_coin(user_id=user_id)
        cursor.execute(f"update bag set coins={now_coin-512} where id={user_id}")
        cursor.execute(f"select invitation from bag where id={user_id}")
        now_invitation=cursor.fetchall()
        now_invitation=now_invitation[0][0]
        cursor.execute(f"update bag set invitation={now_invitation+1} where id={user_id}")
        connect.commit()
        cursor.close()
        connect.close()
        return True
    else:
        with open(indexfile2,encoding='utf-8') as fp:
            index=json.load(fp)
            n=index["shop"][buy-1]["n"]
            price=index["shop"][buy-1]["price"]

        connect=sqlite3.connect(commondb)
        cursor=connect.cursor()
        now_coin=get_coin(user_id=user_id)
        now_coin=now_coin-price
        cursor.execute(f"select {n} from user where id={user_id}")
        nn=cursor.fetchall()
        nn=nn[0][0]
        print(type(n),type(nn+1))
        cursor.execute(f"update user set {n}={nn+1} where id={user_id}")
        cursor.execute(f"update bag set coins={now_coin} where id={user_id}")
        connect.commit()
        cursor.close()
        connect.close()
        return True
