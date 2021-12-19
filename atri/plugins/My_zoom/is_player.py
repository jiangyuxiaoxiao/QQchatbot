import sqlite3

commondb = './Bot_data/My_zoom/common.db'


def isplayer(user_id):
    # 连接数据库
    connect = sqlite3.connect(commondb)
    # 创建游标
    cursor = connect.cursor()
    # 查询id
    print(user_id)
    cursor.execute("select * from user where id={}".format(user_id))
    response = cursor.fetchall()
    cursor.close()
    connect.close()
    print(response)
    if not response:
        return False
    else:
        return True
