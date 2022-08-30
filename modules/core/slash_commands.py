from discord.app_commands import CommandTree

class Module:
    name = "slash_commands"

    def __init__(self,bot):
        self._cmds_synced = False

        self.bot = bot
        self.cmd_tree = None
    
    async def init(self):
        self.cmd_tree = CommandTree(self.bot)
    
    async def postinit(self):
        self.bot.get_module("func_inject").inject(self.on_ready)
    
    async def on_ready(self):
        await self.bot.wait_until_ready()
        if not self._cmds_synced:
            await self.cmd_tree.sync()
            self._cmds_synced = True