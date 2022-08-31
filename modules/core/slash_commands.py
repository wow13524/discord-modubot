from discord.app_commands import CommandTree
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modubot import Bot

class Module:
    name = "slash_commands"

    def __init__(self,bot: 'Bot'):
        self.bot: Bot = bot
        self._cmds_synced: bool = False
        self.cmd_tree: CommandTree[Bot]
    
    async def init(self):
        self.cmd_tree = CommandTree(self.bot)
    
    async def postinit(self):
        self.bot.get_module("func_inject").inject(self.on_ready)
    
    async def on_ready(self):
        await self.bot.wait_until_ready()
        if not self._cmds_synced:
            await self.cmd_tree.sync()
            self._cmds_synced = True