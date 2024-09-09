from pathlib import Path
from .utils import consts
import importlib.util
import importlib
from typing import List
from .config import *
from .config.decorators import *
from . import utils

class Jidouteki():
    def __init__(self, proxy, cache_ttl=180) -> None:
        self.proxy = proxy
        self.cache_ttl = cache_ttl
        self.cache = {}
    
    def load_config(self, path) -> "Config":
            path = Path(path)
            module_name = path.stem
            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            attr = getattr(module, consts.CONFIG_FIELD, None)
            
            if attr: return attr(_context=self)
            else:
                raise Exception(f"Config not found in '{path.name}'. Did you forget to add '@jidouteki.register'?")

    def load_directory(self, dir) -> List[Config]:
        configs = []
        for path in Path(dir).iterdir():
            if path.is_file() and not path.name.startswith("_") and path.suffix == ".py":
                configs.append(self.load_config(path))
        return configs