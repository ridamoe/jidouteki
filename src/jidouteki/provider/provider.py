from ..objects import *
from ..config import ProviderConfig
from typeguard import check_type
from typing import List
import inspect

MAPPINGS_TYPES = {
    "meta": Metadata,
    "match": Dict[str, str] | None,
    "series.chapters": List[Chapter],
    "series.title": str,
    "series.cover": str,
    "images": List[str],
}

class Provider():
    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    def has(self, key):
        """
        Checks if a provider method is availablbe
            
            Example: `provider.has("series.chapter")` will return True / False
            based on whether the provider supports chapter lists
        """
        return self.config._get_mapping(key) != None

    def params(self, key):
        """Returns the parameters of the provider method
            
            Example: `provider.params("series.chapter")` returns the list
            of keyword parameters for `provider.series.chapter()`
        """
        func = self.config._get_mapping(key)
        if func:
            signature = inspect.signature(func)
            args = [
                param.name for param in signature.parameters.values()
            ]
            return args[1:]
        else: return []

    def _get(self, key, **kwargs):
        func = self.config._get_mapping(key)
        
        params = self.params(key)
        kwargs  = {key: value for key,value in kwargs.items() if key in params} 
        value = func(self.config, **kwargs)
        type = MAPPINGS_TYPES.get(key, None)
        if type:
            try:
                check_type(value, type)
            except Exception as e:
                file_path = inspect.getfile(func)
                source_lines, line_number = inspect.getsourcelines(func)
                function_name = func.__name__
                
                # Format the output
                e.add_note(f"  File \"{file_path}\", line {line_number}, in {function_name}\nType check failed for @jidouteki.{key}. Check your return type")
                raise e

        return value
    
    class Series:
        def __init__(self, provider: "Provider"):
            self.provider = provider

        def title(self, **kwargs) -> str:
            return self.provider._get("series.title", **kwargs)

        def chapters(self, **kwargs) -> List[Chapter]:
            return self.provider._get("series.chapters", **kwargs)

        def cover(self, **kwargs) -> str:
            return self.provider._get("series.cover", **kwargs)

    @property
    def series(self):
        return Provider.Series(self)
    
    @property
    def meta(self) -> Metadata:
        return self.config.meta

    def match(self, url):
        return self._get("match", url=url)
        
    def images(self, **kwargs) -> List[str]:
        return self._get("images", **kwargs)

    class Search:
        def __init__(self, provider: "Provider"):
            self.provider = provider

    @property
    def search(self):
        return Provider.Search(self)