from pathlib import Path
import importlib.util
import importlib
import inspect
from typing import List
from .provider import *
from .parser import *
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
            
            website_parser = None
            
            for _, klass in inspect.getmembers(module, inspect.isclass):
                if issubclass(klass, WebsiteParser) and klass is not WebsiteParser:
                    if website_parser != None:
                        raise Exception(f"Multiple parsers found in '{path.name}'. Only a single parser should be defined per file.")
                    else:
                        website_parser = klass
            
            if not website_parser:
                raise Exception(f"No parser found in '{path.name}'. Create a class that inherits from 'WebsiteParser'")
                 
            return Provider(website_parser(context=self))

    def load_directory(self, dir) -> List[Provider]:
        providers = []
        for path in Path(dir).iterdir():
            if path.is_file() and not path.name.startswith("_") and path.suffix == ".py":
                providers.append(self.load_provider(path))
        return providers