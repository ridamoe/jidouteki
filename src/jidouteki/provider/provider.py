from ..objects import *
from ..config import ProviderConfig
from typeguard import check_type
from typing import List
from .get import ProviderGet
from .has import ProviderHas
from .params import ProviderParams
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
        
        self.has = ProviderHas(config)
        """
        Checks if a provider method is availablbe
        """
        
        self.params = ProviderParams(config)
        """
        Returns the parameters of the provider method
        """
    
    @property
    def meta(self) -> Metadata:
        return self.config.meta