from __future__ import annotations
 
# pyright: reportUnknownVariableType=false
# ^ the type of typeguard.check_type ironically can't be inferred :P

import json
import os
from typeguard import check_type
from typing import Any,Dict,Generator,Tuple,get_origin

class Config:
    def __init__(self,config_path: str) -> None:
        self.path: str = config_path
        self.exists: bool = os.path.exists(config_path)

        if self.exists:
            with open(config_path) as f:
                self._load(json.load(f))
        else:
            self._load({})
            self.save()
            raise Exception(f"config does not exist, new one created at '{config_path}'")
    
    def _load(self,data: Dict[str,Any]) -> None:
        needs_saving: bool = False
        for attr,t in self.__annotations__.items():
            value: type
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
        with open(self.path,"w+") as f:
            json.dump(dict(self),f,indent=4)
    
    def __iter__(self) -> Generator[Tuple[str,Any],None,None]:
        for attr in self.__annotations__.keys():
            yield attr, getattr(self,attr)