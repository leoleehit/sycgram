import asyncio
import re

from core import command
from loguru import logger
from pyrogram import Client
from pyrogram.errors import FloodWait, RPCError
from pyrogram.types import Message
from tools.helpers import delete_this, escape_markdown
from tools.sessions import session


@Client.on_message(command(['biss', 'diss', 'tg']))
async def other(_: Client, msg: Message):
    """喷人/舔狗"""
    if bool(re.match(r"-(d|b)iss", msg.text)):
        symbol = '💢 '
        api = 'https://zuan.shabi.workers.dev/'
    elif bool(re.match(r"-tg", msg.text)):
        symbol = '👅 '
        api = 'http://ovooa.com/API/tgrj/api.php'

    await msg.edit_text(f"{symbol}It's preparating.")

    for _ in range(10):
        try:
            resp = await session.get(api, timeout=5.5)
            if resp.status == 200:
                text = escape_markdown(await resp.text())
            else:
                resp.raise_for_status()
        except Exception as e:
            logger.error(e)
            continue

        words = f"{msg.reply_to_message.from_user.mention(style='md')} {text}" \
            if msg.reply_to_message else text
        try:
            await msg.edit_text(words, parse_mode='md')
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await msg.edit_text(words, parse_mode='md')
        except RPCError as e:
            logger.error(e)

        await logger.complete()
        return

    # Failed to get api text
    await delete_this(msg)
    res = await msg.edit_text('😤 Rest for a while.')
    await asyncio.sleep(3)
    await delete_this(res)
