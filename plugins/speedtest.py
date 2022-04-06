import asyncio
import re

from core import command
from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from tools.constants import SPEEDTEST_RUN
from tools.helpers import Parameters, delete_this, get_cmd_error, show_error
from tools.speedtests import Speedtester


@Client.on_message(command('speedtest'))
async def speedtest(_: Client, msg: Message):
    """服务器测速，用法：-speedtest <节点ID|list|update>"""
    cmd, opt = Parameters.get(msg)

    await msg.edit_text("⚡️ Speedtest is running.")
    async with Speedtester() as tester:
        if opt == 'update':
            try:
                update_res = await tester.init_for_speedtest('update')
            except asyncio.exceptions.TimeoutError:
                await msg.edit_text("⚠️ Update Timeout")
            except Exception as e:
                await show_error(msg, e)
            else:
                # TODO：有个未知错误
                await msg.edit_text(f"Result\n```{update_res}```")
            return
        elif opt == 'list':
            try:
                text = await tester.list_servers_ids(f"{SPEEDTEST_RUN} -L")
                await msg.edit_text(text, parse_mode='md')
            except asyncio.exceptions.TimeoutError:
                await msg.edit_text("⚠️ Speedtest Timeout")
            return
        elif bool(re.match(r'[0-9]+', opt)) or not opt:
            try:
                text, link = await tester.running(
                    f"""{SPEEDTEST_RUN}{'' if not opt else f' -s {opt}'}"""
                )
            except asyncio.exceptions.TimeoutError:
                await msg.edit_text("⚠️ Speedtest Timeout")
                return
        else:
            await msg.edit_text(get_cmd_error(cmd))
            return

    if not link:
        await msg.edit_text(text)
        return

    # send speed report
    try:
        await msg.reply_photo(photo=link, caption=text, parse_mode='md')
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await msg.reply_photo(photo=link, caption=text, parse_mode='md')
    except Exception as e:
        await show_error(msg, e)
    # delete cmd history
    await delete_this(msg)
