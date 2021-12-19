from nonebot.rule import Rule
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State


def baiduyixia_rulee():
    async def baiduyixia_rule(bot: Bot, event: Event, state: T_State) -> bool:
        msg = event.raw_message
        if "查一下" in msg or "百度" in msg:
            return True

    return Rule(baiduyixia_rule)
