from ..objects import *
from ..parser import WebsiteParser
from typeguard import check_type
from typing import List
from .get import ProviderGet
from .has import ProviderHas
from .test import ProviderTest
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
    def __init__(self, parser: WebsiteParser) -> None:
        self.parser = parser
        self.get = ProviderGet(parser)
        
        self.has = ProviderHas(parser)
        """
        Checks if a provider method is availablbe
        """
        
        self.params = ProviderParams(parser)
        """
        Returns the parameters of the provider method
        """
        
        self.test = ProviderTest(parser)
        """
        Run self tests defined by providers
        """
    
    @property
    def meta(self) -> Metadata:
        return self.parser.meta