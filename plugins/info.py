from core import command
from pyrogram import Client
from pyrogram.types import Message
from tools.helpers import get_fullname


@Client.on_message(command("id"))
async def get_id(_: Client, msg: Message):
    """直接使用或者回复目标消息，从而获取各种IDs"""
    text = f"Message ID: `{msg.message_id}`\n\n" \
           f"Chat Title: `{msg.chat.title}`\n" \
           f"Chat Type: `{msg.chat.type}`\n" \
           f"Chat ID: `{msg.chat.id}`"

    if msg.reply_to_message:
        user = msg.reply_to_message.from_user
        text = f"Repiled Message ID: `{msg.reply_to_message.message_id}`\n\n" \
               f"User Nick: `{get_fullname(user)}`\n"\
               f"User Name: `@{user.username}`\n" \
               f"User ID: `{user.id}`\n\n" \
               f"{text}"

    await msg.edit_text(text)
