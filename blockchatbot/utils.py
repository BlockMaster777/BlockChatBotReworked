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

# coding=utf8

from configparser import ConfigParser
from enum import Enum
from dotenv import load_dotenv
import os


class Privilege(Enum):
    ASK = "can_ask"
    TEACH = "can_teach"
    REMOVE = "can_remove"
    MODERATE = "can_moderate"
    ADMIN = "can_admin"
    


def get_db_config():
    load_dotenv()
    return {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD")
        }
