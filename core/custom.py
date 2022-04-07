#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   custom.py
@Time    :   2022/04/02 10:17:03
@Author  :   Viperorz
@Version :   1.0.0
@License :   (C)Copyright 2021-2022
@Desc    :   None
"""


from typing import Any, Dict

import yaml
from pyrogram import filters
from pyrogram.types import Message
from tools.constants import STORE_TRACE_DATA
from tools.storage import SimpleStore

command_data: Dict[str, Any] = yaml.full_load(open("./data/command.yml", 'rb'))


def command(key: str):
    """匹配UserBot指令"""
    # 指令前缀
    # 例一：prefixes = "-"
    # 例二：prefixes = ["-", "/", "+"]
    prefixes = command_data.get('help').get('all_prefixes')
    cmd = command_data.get(key).get('cmd')
    return filters.me & filters.text & filters.command(cmd, prefixes)


def is_traced():
    """正则匹配用户输入指令及参数"""
    async def func(flt, _, msg: Message):
        async with SimpleStore(auto_flush=False) as store:
            trace_data = store.get_data(STORE_TRACE_DATA)
            if not trace_data:
                return False
            elif not trace_data.get(msg.from_user.id):
                return False
            return True

    # "data" kwarg is accessed with "flt.data" above
    return filters.incoming & filters.create(func)
