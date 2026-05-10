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

import psycopg2
from .utils import get_config


class DatabaseManager:
    def __init__(self):
        self.config = get_config()
    
    async def _connect(self) -> psycopg2.extensions.connection:
        return psycopg2.connect(**self.config)
    
    @staticmethod
    async def _cursor(connection) -> psycopg2.extensions.cursor:
        return connection.cursor()
    
    async def _execute(self, statement, parameters):
        with await self._connect() as connection:
            cursor = await self._cursor(connection)
            cursor.execute(statement, parameters)
            connection.commit()
    
    async def _select(self, statement, parameters) -> list[tuple]:
        with await self._connect() as connection:
            cursor = await self._cursor(connection)
            cursor.execute(statement, parameters)
            return cursor.fetchall()
    
    async def add_user(self, tgid: int):
        await self._execute("INSERT INTO users (tgid) "
                            "VALUES (%s) RETURNING id;", (tgid,))
    
    async def remove_user(self, tgid: int):
        await self._execute("DELETE FROM users WHERE tgid = %s", (tgid,))
    
    async def info_user(self, tgid: int):
        data = (await self._select("SELECT * FROM users WHERE tgid = %s",
                                 (tgid,)))[0]
        return {
            "id": data[0],
            "tgid": data[1],
            "can_ask": data[2],
            "can_teach": data[3],
            "can_remove": data[4],
            "can_moderate": data[5],
            "can_admin": data[6],
            }
