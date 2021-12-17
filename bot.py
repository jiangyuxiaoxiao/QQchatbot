#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
#
#
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
from load_dictionary import dictionary_initial
import json
import sys
sys.path.append("./atri/plugins")
# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function

# 初始化nonebot
nonebot.init()
app = nonebot.get_asgi()
# 以创建一个新进程运行cqhttp，与之对应的，os.system("cqhttp.exe")会阻塞至程序运行结束
# os.popen("cqhttp.exe")
# 连接驱动
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
#载入词库
dictionary_initial()
# Please DO NOT modify this file unless you know what you are doing!
# As an alternative, you should use command `nb` or modify `pyproject.toml` to load plugins
# 初始化插件
nonebot.load_from_toml("pyproject.toml")
# 根据插件自定义目录进行初始化
plugin_dir = "./Bot_data/Plugins_dir/plugin.json"
with open(plugin_dir, encoding="utf-8") as plg_dir:
    plugins = json.load(plg_dir)
    plugins = plugins["Plugin"]["Dir"]
    for plugin in plugins:
        nonebot.load_plugin(plugin)
# Modify some config / config depends on loaded configs
# 
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")

    nonebot.run(app="__mp_main__:app")

