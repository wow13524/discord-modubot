class Module:
    name = "command_shutdown"

    def __init__(self,bot):
        self.bot = bot
    
    async def postinit(self):
        cmd_tree = self.bot.get_module("slash_commands").cmd_tree

        @cmd_tree.command(name="shutdown",description="Stops the bot.")
        async def shutdown(interaction):
            await interaction.response.send_message("x.x")
            await self.bot.close()