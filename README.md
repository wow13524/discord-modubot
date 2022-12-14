# Modubot

A simple, lightweight API wrapper for [discord.py](https://github.com/Rapptz/discord.py)'s AutoShardedClient written in Python.

---

## Key Features
- Modular behavior support
    - Hook into core client events with [`modules.core.func_inject`](https://github.com/wow13524/discord-modubot/tree/main/modules/core)
    - Simple embedded database implementation with [`modules.persistence`](https://github.com/wow13524/discord-modubot/tree/main/modules/persistence)
    - Modules can interact with each other using `Bot.get_module()`
- Integrated config file
    - Control intents, enabled modules, and bot token
    - Integration with module subconfig sections
- Multiple instance support
    - Easily run different bots from the same script
    - Behaviors are defined in config files
- Fully type annotated
    - Leveraged for easy subconfig sections

## Getting Started

Populate `BotConfig.token` in the provided [`example_config.json`](https://github.com/wow13524/discord-modubot/tree/main/example_config.json) and run either [`main.py`](https://github.com/wow13524/discord-modubot/tree/main/main.py) or the following code within the same directory:

```py
from modubot import Bot

Bot(config_name="example_config.json").run()
```
The bot should connect to Discord with the slash command `/shutdown` enabled.

## Running Multiple Instances

Multiple bots can be started from the same script in a similar manner to discord.py's Client.  
Different bot configurations can be passed into the Bot constructor in order to do this.  
An example can be found at [`multi_instance.py`](https://github.com/wow13524/discord-modubot/tree/main/multi_instance.py) with configs located in [`example_configs`](https://github.com/wow13524/discord-modubot/tree/main/example_configs).

## Creating Modules

A module should follow this structure:
```py
from modubot import ModuleBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modubot import Bot

class Module(ModuleBase):
    def __init__(self,bot: 'Bot') -> None:
        ...

    async def init(self) -> None:       #This method is optional to implement.
        ...
    
    async def postinit(self) -> None:   #This method is optional to implement.
        ...
```
Modules are instantiated once during bot startup and these singletons remain active during the runtime of the bot.  
*Note: Type annotations are not required for modules, yet highly encouraged.*

> ### `__init__` Constructor:
> **Parameters:**
> - **Bot** (`modubot.Bot`) - The active bot instance, useful for accessing `Bot.config` or `Bot.get_module()`.  
> 
> Intended for accessing `bot.config` or initializing any instance variables belonging to the module.  
> *Note: At this stage, `bot` has not been initialized as an `AutoSharedClient`.*
>
> ### `init` Method:
> An `async` method intended for interfacing with the bot.
>
> ### `postinit` Method:
> An `async` method intended for interfacing with other modules.

## Module Config Integration
**The following types are currently supported for module configs:**
- `bool`
- `int`
- `float`
- `str`
- `typing.Literal`
- `typing.List`
- `typing.Dict`
- `modubot.PropertyDict`

A module's configuration should follow this structure:
```py
from modubot import PropertyDict

class ExampleConfig(PropertyDict):
    foo: int = 10
    bar: str = "asdf"
    baz: bool = True
```
*Note: Type annotations are required for module configs and are automatically enforced when the config file is read.*

Module configs can be retrieved during any stage of module initialization as follows:
```py
from .example_config import ExampleConfig

... #Module class definition
    def __init__(self,bot: 'Bot') -> None:
        self._bot: Bot = bot
        self._config: ExampleConfig = self._bot.config.get(ExampleConfig)

        print(self._config.foo)  #int
        print(self._config.bar)  #str
        print(self._config.baz)  #bool
...
```
Module config sections are appended to the config file if they don't already exist and are populated with the values defined in the module config class.  The name of the section within the config file is the same as the name of the class representing it.

An example module can be found at [`modules.example_module`](https://github.com/wow13524/discord-modubot/tree/main/modules/example_module).