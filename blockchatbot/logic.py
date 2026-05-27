# coding=utf-8

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

from aiogram.types import Message
from .dbm import DatabaseManager
from .utils import Privilege


dbm = DatabaseManager()


async def check_privileges(tgid: int, privilege: Privilege):
    return (await dbm.info_user(tgid))[privilege.value]


async def can_ban_user(actor_tgid: int, user_tgid: int):
    if await check_privileges(user_tgid, Privilege.ADMIN):
        return False
    
    if not await check_privileges(actor_tgid, Privilege.MODERATE):
        return False
    return True
