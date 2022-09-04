from modubot import ModuleBase
from typing import TYPE_CHECKING
from .example_config import ExampleConfig

if TYPE_CHECKING:
    from modubot import Bot
    from ..core.func_inject import Module as FuncInject

class Module(ModuleBase):
    def __init__(self,bot: 'Bot') -> None:
        """
        Initialize any necessary instance variables for the module.
        """
        self.bot: Bot = bot
        self.config: ExampleConfig = self.bot.config.get(ExampleConfig)

        print(self.config.foo)  #int
        print(self.config.bar)  #str
        print(self.config.baz)  #bool

    async def init(self) -> None:
        """
        Interface with the bot after the client has been initialized.
        """
        print("Is the bot ready?",self.bot.is_ready())
    
    async def postinit(self) -> None:
        """
        Interface with other modules after they have been initialized.
        """
        func_inject: FuncInject = self.bot.get_module("modules.core.func_inject")
        func_inject.inject(self.on_ready)
    
    async def on_ready(self) -> None:
        print("example_module successfully hooked into bot.on_ready()!")