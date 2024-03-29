import asyncio
from inspect import Parameter

from loguru import logger

from core import command
from pyrogram import Client
from pyrogram.errors import FloodWait, RPCError
from pyrogram.types import Message
from tools.helpers import delete_this, get_cmd_error, kick_one


@Client.on_message(command('sb'))
async def sb(cli: Client, msg: Message):
    """回复一条消息，将在所有共同且拥有管理踢人权限的群组中踢出目标消息的主人"""
    cmd, *_ = Parameter.get(msg)
    reply_to_message = msg.reply_to_message
    if not reply_to_message or msg.chat.type in ['bot', 'private']:
        await msg.edit_text(get_cmd_error(cmd))
        return

    counter, target = 0, reply_to_message.from_user
    common_groups = await target.get_common_chats()
    logger.info(
        f"Start to kick <{target.first_name}{target.last_name} <{target.id}>")
    for chat in common_groups:
        try:
            if await kick_one(cli, chat.id, target.id):
                counter = counter + 1

        except FloodWait as e:
            await asyncio.sleep(e.x)
            if await kick_one(cli, chat.id, target.id):
                counter = counter + 1
                logger.success(
                    f"Kick this user out of <{chat.tile} {chat.id}>"
                )

        except RPCError as e:
            logger.warning(
                f"No admin rights in this group <{chat.title} {chat.id}>")
            logger.warning(e)

    # delete this user all messages
    await cli.delete_user_history(msg.chat.id, target.id)

    # Inform
    text = f"😂 Kick {target.mention(style='md')} in {counter} common groups."
    await msg.edit_text(text)
    await asyncio.sleep(10)
    await delete_this(msg)
    # log
    logger.success(f"{cmd} | {text}")
    await logger.complete()
