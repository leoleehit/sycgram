import asyncio
from getpass import getuser
from io import BytesIO
from platform import node

from core import command
from pyrogram import Client
from pyrogram.types import Message
from tools.helpers import Parameters, basher, delete_this, get_cmd_error


@Client.on_message(command("sh"))
async def shell(_: Client, msg: Message):
    """执行shell脚本"""
    cmd, _input = Parameters.get(msg)
    if not _input:
        await msg.edit_text(get_cmd_error(cmd))
        return

    try:
        res = await basher(_input, timeout=30)
    except asyncio.exceptions.TimeoutError:
        await msg.edit_text('❗️ Connection Timeout')
        return

    _output: str = res.get('output') if not res.get('error') else res.get('error')
    header = f"**{getuser()}@{node()}**\n"
    all_bytes = len(header.encode() + _input.encode() + _output.encode())
    if all_bytes >= 2048:
        await delete_this(msg)
        await msg.reply_document(
            document=BytesIO(_output.encode()),
            caption=f"{header}> # `{_input}`",
            file_name="output.log",
            parse_mode='md'
        )
        return

    await msg.edit_text(
        f"{header}> # `{_input}`\n```{_output.strip()}```",
        parse_mode='md'
    )
