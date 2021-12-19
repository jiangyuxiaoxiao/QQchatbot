import sqlite3
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
import json

indexname = ".\\Bot_data\\My_zoom\\pat.json"
cmdb = ".\\Bot_data\\My_zoom\\common.db"


def register(id, name='未取名'):
    # 连接数据库
    connect = sqlite3.connect(cmdb)
    # 创建游标
    cursor = connect.cursor()

    cursor.execute("select id from user where id={}".format(id))

    if len(list(cursor)):
        cursor.close()
        connect.close()
        return f'''
        {name}
        你已经是宠物乐园的一员。'''

    # 注意，这里必须是一个元组
    info_tuple = (id,name)
    cursor.execute('''INSERT INTO user(ID,name)
                    VALUES (?,?)''', info_tuple)
    connect.commit()

    cursor.execute("select id from user where id={}".format(id))

    if len(list(cursor)):
        cursor.close()
        connect.close()
        return f'''
        🎊🎊🎉🎉🎊🎊
        {name}
        注册成功！
        欢迎加入宠物乐园！
        🎊🎊🎉🎉🎊🎊
        '''

    # with open(file=indexname, encoding="utf-8") as fp:
    #     index = json.load(fp)
    #     datas = index["data"]
    #     print(datas)
    #
    # data_msg=""
    #
    # for data in datas:
    #     data_msg=data_msg+data+','
