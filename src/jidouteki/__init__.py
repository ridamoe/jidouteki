from pathlib import Path
import importlib.util
import importlib
import inspect
from typing import List
from .provider import *
from .config import *
from .utils import *

class Jidouteki():
    def __init__(self, proxy, cache_ttl=180) -> None:
        self.proxy = proxy
        self.cache_ttl = cache_ttl
    
    def load_provider(self, path) -> "Provider":
            path = Path(path)
            module_name = path.stem
            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            provider_config = None
            
            for _, klass in inspect.getmembers(module, inspect.isclass):
                if issubclass(klass, ProviderConfig) and klass is not ProviderConfig:
                    if provider_config != None:
                        raise Exception(f"Multiple provider configs found in '{path.name}'. Only a single provider can be defined per file.")
                    else:
                        provider_config = klass
            
            if not provider_config:
                raise Exception(f"No provider config found in '{path.name}'. Create a class that inherits from 'ProviderConfig'")
                 
            return Provider(provider_config(context=self))

    def load_directory(self, dir) -> List[Provider]:
        configs = []
        for path in Path(dir).iterdir():
            if path.is_file() and not path.name.startswith("_") and path.suffix == ".py":
                configs.append(self.load_provider(path))
        return configs