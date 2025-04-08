from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Metadata():
    key: str 
    display_name: str
    base: str = field(default=None)
    languages: list = field(default=None)

@dataclass
class Chapter():
    params: Dict[str, str]
    chapter: str 
    volume: str = field(default=None)
    title: str = field(default=None)
    language: str = field(default=None)