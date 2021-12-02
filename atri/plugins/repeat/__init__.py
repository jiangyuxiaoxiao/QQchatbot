import random

from nonebot import on_message,on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event


user_counters = {}

class UserCounter:
    """用于计算复读次数"""
    def __init__(self, qid):
        self.qid = qid
        self.count = 0
        self.probabilty = 0

    def counts(self):
        return self.count

    def probability(self):
        return self.probabilty

    def set_count(self,count):
        self.count = count
        return

    def set_probability(self,probabilty):
        self.probabilty = probabilty
        return


msg_counter = on_message(priority=240, block=False)
msg_count_checker = on_command("复读", priority= 239, block=False)


@msg_counter.handle()
async def msg_counter(bot: Bot, event: Event, state: T_State):
    if event.post_type == "message":
        if event.message_type == "group":
            user_id = event.user_id
            user = str(user_id)
            group_id = event.group_id
            msg = event.raw_message
            # 排除指令语句
            if "#" in msg or "/" in msg or "复读" in msg:
                return
            # 查找是否已计数
            global user_counters
            check = user_counters.get(user)
            if check == None:
                user_counters[user] = UserCounter(user_id)
            else:
                probabilty = user_counters[user].probability()
                count = user_counters[user].counts()
                probnum = random.randint(1,1000)
                if probabilty >= probnum :
                    user_counters[user].set_probability(0)
                    user_counters[user].set_count(0)
                    msg.replace("你", "他")
                    msg.replace("我","你")
                    msg.replace("亚托莉","你")
                    await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
                    return
                else:
                    count = count + 1
                    probabilty = probabilty + count * 0.125
                    if probabilty > 1000:
                        probabilty = 1000
                    user_counters[user].set_probability(probabilty)
                    user_counters[user].set_count(count)
                    return


@msg_count_checker.handle()
async def msg_counter_checker(bot: Bot, event: Event, state: T_State):
    if event.post_type == "message":
        if event.message_type == "group":
            user_id = event.user_id
            user = str(user_id)
            group_id = event.group_id
            user_name = event.sender.nickname
            # 查找是否已计数
            global user_counters
            check = user_counters.get(user)
            if check == None:
                user_counters[user] = UserCounter(user_id)
            probabilty = user_counters[user].probability()
            the_count = user_counters[user].counts()
            str_probabilty = "%.3f"%(probabilty/10)
            msg = "啊啊啊！亚托莉不是复读机！\n当前已计数{}，{}复读概率{}%".format(the_count,user_name,str_probabilty)
            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})


