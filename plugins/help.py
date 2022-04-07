from typing import Any, Dict
import yaml
from core import command
from pyrogram import Client
from pyrogram.types import Message
from tools.helpers import Parameters


@Client.on_message(command('help'))
async def helper(_: Client, msg: Message):
    """指令用法提示。格式：-help <cmd|None>"""
    helper_cmd, cmd = Parameters.get(msg)
    cmd_data: Dict[str, Any] = yaml.full_load(open('./data/command.yml', 'rb'))
    if not cmd:
        tmp = '、'.join(f"`{k}`" for k in cmd_data.keys())
        text = f"📢 **指令列表：**\n{tmp}\n\n**发送** `{helper_cmd} <{cmd}>` **查看某指令的详细用法**"
    elif not cmd_data.get(cmd):
        text = f'❓ `{cmd}` 404 Not Found'
    else:
        text = f"格式：`{cmd_data.get(cmd).get('format')}`\n" \
               f"用法：`{cmd_data.get(cmd).get('usage')}`"
    await msg.edit_text(text, parse_mode='md')
