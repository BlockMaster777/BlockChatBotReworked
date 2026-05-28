# coding=utf8

#  BlockChatBotReworked
#  Copyright (C) 2026  BlockMaster
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import aiogram as aio
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import blockchatbot.logic as lg
import asyncio
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# noinspection PyTypeChecker
TOKEN: str = os.getenv("BOT_TOKEN")
if TOKEN is None:
    raise ValueError("BOT_TOKEN environment variable not found")

dp = aio.Dispatcher()


def auto_register(func):
    async def wrapper(message: Message):
        if not await lg.dbm.check_registered(message.from_user.id):
            await lg.dbm.add_user(message.from_user.id)
        await func(message)
    return wrapper


async def ban_user(message: Message, tgid: int):
    if await lg.can_ban_user(message.from_user.id, tgid):
        await lg.dbm.ban_user(tgid)
        await message.reply("💥 **BAN!**")
    else:
        await message.reply("⚠️ Cant ban user")


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.reply(f"👋 Hello, {message.from_user.full_name}\\.\n"
                        f"**I \\.\\.\\. AM BLOCK CHATBOT\\!**\n"
    f"[Source code](https://github.com/BlockMaster777/BlockChatBotReworked)\n"
    f"[Creator](https://github.com/BlockMaster777)\n"
    f"[Bug reports](https://github.com/BlockMaster777/BlockChatBotReworked/issues)\n",
                        parse_mode=ParseMode.MARKDOWN_V2,
                        disable_web_page_preview=True)


@dp.message(Command("me"))
@auto_register
async def info_handler(message: Message):
    tgid = message.from_user.id
    info = await lg.dbm.info_user(tgid)
    answer_text = (f"ℹ️ @{message.from_user.username}\n"
                   f"🆔 ID: {info["id"]}\n"
                   f"🪪 Telegram ID: {info['tgid']}\n"
                   f"🗣️ Can ask: {info['can_ask']}\n"
                   f"🧑‍🏫 Can teach: {info['can_teach']}\n"
                   f"❌ Can remove: {info['can_remove']}\n"
                   f"💥 Is moderator: {info['can_moderate']}\n"
                   f"🧑‍💻 Is admin: {info['can_admin']}")
    await message.answer(answer_text)


@dp.message(Command("light_ban"))
@auto_register
async def id_ban_handler(message: Message):
    if message.reply_to_message:
        tgid = message.reply_to_message.from_user.id
        await ban_user(message, tgid)
        return
    try:
        ban_id = int(message.text.split()[1])
    except IndexError:
        await message.reply("⚠️ No user id provided\n"
                            "💬 You can reply to message to ban user")
        return
    except ValueError:
        await message.reply("⚠️ Wrong id format")
        return
    if not await lg.dbm.check_registered(ban_id):
        await message.reply("⚠️ ID is not registered")
        return
    await ban_user(message, ban_id)
    
    

async def main():
    bot = aio.Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
