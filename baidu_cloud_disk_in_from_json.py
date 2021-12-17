import sqlite3
import json

def load_data_to_db():
    # 连接数据库
    connect = sqlite3.connect("./Bot_data/SQLite/BaiduCloudDisk.db")
    # 创建游标
    cursor = connect.cursor()
    # 读取词库目录索引文件
    with open(indexname, encoding="utf-8") as index_file:
        index = json.load(index_file)
        index = index['index']
        print(index)

        # 遍历读取每个json
        for disk in index:
            with open(disk, encoding="utf-8") as disk_file:
                disk_piece = json.load(disk_file)
                #遍历插入数据库
                for info_name in disk_piece:
                    info = disk_piece[info_name]
                    ID = info["ID"]
                    NAME = info["NAME"]
                    URL = info["URL"]
                    KEY = info["KEY"]
                    ZIPKEY = info["ZIPKEY"]
                    INFO = info["INFO"]
                    TYPE = info["TYPE"]
                    id_tuple = (ID,)
                    cursor.execute("SELECT COUNT(*) FROM BAIDU WHERE ID=(?)", id_tuple)
                    for c in cursor:
                        if c[0] == 0:
                            info_tuple=(ID, NAME, URL, KEY, ZIPKEY, INFO, TYPE)
                            cursor.execute('''
                                            INSERT INTO BAIDU(ID,NAME,URL,KEY,ZIPKEY,INFO,TYPE)
                                            VALUES (?,?,?,?,?,?,?)''', info_tuple)
        # 数据库保存更新
        cursor.close()
        connect.commit()
        connect.close()
        print("录入完毕")


indexname = "./Bot_data/BaiduCloudDisk/index.json"
load_data_to_db()

