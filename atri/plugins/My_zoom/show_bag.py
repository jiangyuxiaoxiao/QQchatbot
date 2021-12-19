import json
import sqlite3

commondb = "./Bot_data/My_zoom/common.db"
indexfile = "./Bot_data/My_zoom/bag.json"


def show_bagg(user_id):
    connect = sqlite3.connect(commondb)
    cursor = connect.cursor()
    cursor.execute("select * from bag where id={}".format(user_id))
    result = cursor.fetchall()[0]
    print(result)

    with open(indexfile, encoding="utf-8") as fp:
        index = json.load(fp)
        index=index["name"]

    msg = result[1] + ',你背包中有：\n'

    print(index)
    ind=index[2:]
    for name in ind:
        msg=msg+name+':'+str(result[index.index(name)])+'\n'
        print(msg)

    return msg
