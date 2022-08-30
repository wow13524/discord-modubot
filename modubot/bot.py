import discord
import importlib
import os
from .config import Config

DEFAULT_CONFIG_NAME = "config.json"

class Bot(discord.AutoShardedClient):
    def __init__(self,work_dir=os.getcwd(),config_name=DEFAULT_CONFIG_NAME):
        self.work_dir = work_dir
        self.config = Config(config_path=os.path.join(work_dir,config_name))
        self.loaded_modules = self._preload_modules()

        intents = discord.Intents.default()
        for intent,value in self.config.intents.items():
            assert hasattr(intents,intent) and type(getattr(intents,intent)) == bool, f"invalid intent '{intent}' present in config"
            setattr(intents,intent,bool(value))
        super().__init__(intents=intents)
    
    def _preload_modules(self):
        loaded_modules = {}
        name_path_dict = {}
        for module_path in self.config.enabled_modules:
            module = importlib.import_module(module_path).Module
            module_name = module.name
            if module_name in name_path_dict:
                raise Exception(f"modules '{name_path_dict[module_name]}' and '{module_path}' share the same name '{module_name}'")
            else:
                name_path_dict[module_name] = module_path
                loaded_modules[module_name] = module(self)
        return loaded_modules
    
    def get_module(self,module_name):
        if module_name in self.loaded_modules:
            return self.loaded_modules[module_name]
        else:
            raise Exception(f"cannot find module '{module_name}'")

    async def start(self,token,reconnect=True):
        for module_instance in self.loaded_modules.values():
            if hasattr(module_instance,"init") and callable(module_instance.init):
                await module_instance.init()
        for module_instance in self.loaded_modules.values():
            if hasattr(module_instance,"postinit") and callable(module_instance.postinit):
                await module_instance.postinit()
        await super().start(token,reconnect=reconnect)
    
    def run(self):
        assert self.config.token, "token missing from config"
        super().run(self.config.token)