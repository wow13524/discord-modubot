# pyright: reportUnknownVariableType=false
# ^ the type of typeguard.check_type ironically can't be inferred :P

import json
import os
from typeguard import check_type
from typing import Any,Dict,Generator,Tuple,get_origin,get_type_hints

class Config:
    def __init__(self,config_path: str) -> None:
        self.exists: bool = os.path.exists(config_path)
        self.path: str = config_path
        self.types: Dict[str,Any] = get_type_hints(self)

        if self.exists:
            with open(config_path) as f:
                self._load(json.load(f))
        else:
            self._load({})
            self.save()
            raise Exception(f"config does not exist, new one created at '{config_path}'")
    
    def _load(self,data: Dict[str,Any]) -> None:
        needs_saving: bool = False
        for attr,t in self.types.items():
            value: Any
            if not attr in data:
                print(f"field '{attr}' missing from config, updating")
                value = (get_origin(t) or t)()
                needs_saving = True
            else:
                value = data[attr]
                check_type(f"Config.{attr}",value,t)
            setattr(self,attr,value)
        if needs_saving:
            self.save()
    
    def save(self) -> None:
        existing: Dict[str,Any] = {}
        if os.path.exists(self.path):
            with open(self.path,"r+") as f:
                content: str = f.read()
                if content:
                    existing = json.loads(content)
        with open(self.path,"w+") as f:
            output: Dict[str,Any] = dict(self)
            output.update(existing)
            json.dump(output,f,indent=4)
    
    def __iter__(self) -> Generator[Tuple[str,Any],None,None]:
        for attr in self.types.keys():
            yield attr, getattr(self,attr)