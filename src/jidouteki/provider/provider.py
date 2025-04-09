from ..objects import *
from ..config import ProviderConfig
from typeguard import check_type
from typing import List
from .get import ProviderGet
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
        self.get = ProviderGet(config)

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
        return self.config._get_mapping_params(key)
    
    @property
    def meta(self) -> Metadata:
        return self.config.meta