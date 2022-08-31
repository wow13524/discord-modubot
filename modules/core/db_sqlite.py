import aiosqlite
from os.path import join
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modubot import Bot

DEFAULT_DB_NAME = "data.db"

class Module:
    name = "db_sqlite"

    def __init__(self,bot: 'Bot'):
        self.bot: Bot = bot
        self.db: aiosqlite.Connection
    
    async def init(self):
        self.db = await aiosqlite.connect(join(self.bot.work_dir,DEFAULT_DB_NAME))
    
    async def postinit(self):
        self.bot.get_module("func_inject").inject(self.close)
    
    async def close(self):
        await self.db.close()