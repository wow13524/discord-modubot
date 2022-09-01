# pyright: reportUnusedFunction=false

from discord import Interaction
from discord.app_commands import CommandTree
from modubot import ModuleBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modubot import Bot
    from ..core.slash_commands import Module as SlashCommands

class Module(ModuleBase):
    name = "command_shutdown"

    def __init__(self,bot: 'Bot'):
        self.bot: Bot = bot
    
    async def postinit(self):
        slash_commands: SlashCommands = self.bot.get_module("slash_commands")
        cmd_tree: CommandTree[Bot] = slash_commands.cmd_tree

        @cmd_tree.command(name="shutdown",description="Stops the bot.")
        async def shutdown(interaction: Interaction):
            await interaction.response.send_message("x.x")
            await self.bot.close()