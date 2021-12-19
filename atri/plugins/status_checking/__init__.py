import psutil
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
import math

status_check = on_command("状态查询",priority=240,block=False)


@status_check.handle()
async def status_check(bot: Bot, event: Event, state: T_State):
    cpu_physical_core = psutil.cpu_count(logical=False)
    cpu_logical_core = psutil.cpu_count(logical=True)
    cpu_percent = psutil.cpu_percent()
    cpu_freq = psutil.cpu_freq().max
    memory_total = math.ceil(psutil.virtual_memory().total / (1024 * 1024 * 1024))
    memory_percent = psutil.virtual_memory().percent
    memory_used = psutil.virtual_memory().used / (1024 * 1024 * 1024)
    msg = "CPU核心数{}/{}\nCPU当前占用率{}%\nCPU当前频率{}GHZ\n内存{:.3f}GB/{}GB\n内存当前占用率{}%".format(cpu_physical_core,
    cpu_logical_core, cpu_percent,cpu_freq/1000, memory_used, memory_total,memory_percent)
    if event.message_type == 'group':
        group_id = event.group_id
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    elif event.message_type == 'private':
        user_id = event.user_id
        await bot.call_api("send_private_msg", **{"user_id": user_id, "message": msg})
