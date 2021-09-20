# -*- coding: utf-8 -*-

from typing import List
from pydantic import BaseModel, validator
from pathlib import Path


_conf_file = Path("resources/config/custom.json")

class BtnConfig(BaseModel):
    name: str
    description: str = ""
    hotkey: str = ""
    actions: str = ""
    enable: bool = True
    visible: bool = True

    @validator("actions", pre=True)
    def _btn_actions(cls, value):
        return "\n".join(value.split())


class Configuration(BaseModel):
    buttons: List[BtnConfig] = []

    @staticmethod
    def refresh():
        global config
        config = Configuration.parse_file(_conf_file)

    def save(self):
        _conf_file.parent.mkdir(parents=True, exist_ok=True)
        _conf_file.write_text(self.json(indent=4, ensure_ascii=False), encoding="utf-8")


if _conf_file.exists():
    config = Configuration.parse_file(_conf_file)
else:
    config = Configuration()
