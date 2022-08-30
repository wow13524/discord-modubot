import json
import os

class Config:
    config_fields = {
        "intents": dict,
        "enabled_modules": list,
        "token": str
    }

    def __init__(self,config_path):
        self.exists = False
        self.path = config_path

        if config_path is not None:
            self.exists = os.path.exists(config_path)
            if self.exists:
                with open(config_path) as f:
                    self._load(json.load(f))
            else:
                self._load({x:y() for x,y in self.config_fields.items()})
                self.config.save()
                raise Exception(f"config does not exist, new one created at '{config_path}'")
    
    def _load(self,data):
        fixed = False
        for attr,t in self.config_fields.items():
            value = None
            if not attr in data:
                print(f"field '{attr}' missing from config, updating")
                value = t()
                fixed = True
            else:
                value = data[attr]
                assert type(value) == t, f"expected type {t.__name__} for field '{attr}' in config, got {type(value).__name__}"
            setattr(self,attr,value)
        if fixed:
            self.save()
    
    def save(self):
        with open(self.path,"w+") as f:
            json.dump(dict(self),f,indent=4)
    
    def __iter__(self):
        for attr in self.config_fields.keys():
            yield attr, getattr(self,attr)