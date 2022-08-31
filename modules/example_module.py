from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modubot import Bot

class Module:
    name = "example_module"

    def __init__(self,bot: Bot):
        self.bot = bot
        """
        Initialize any necessary instance variables for the module.
        """

    async def init(self):
        """
        Interface with the bot after the client has been initialized.
        """
    
    async def postinit(self):
        """
        Interface with other modules after they have been initialized.
        """