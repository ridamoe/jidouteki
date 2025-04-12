from typing import List

from ..parser import WebsiteParser
from ..objects import *
from .dispatcher import *

class GetSeries(Dispatcher):
    @dispatched("series.title")
    def title(self, **kwargs) -> str: ...
    
    @dispatched("series.chapters")
    def chapters(self, **kwargs) -> List[Chapter]: ...
    
    @dispatched("series.cover")
    def cover(self, **kwargs) -> str: ...

class GetSearch(Dispatcher):
    pass
    
class ProviderGet(Dispatcher):
    def __init__(self, parser: WebsiteParser) -> None:
        self._parser = parser
        self.series = GetSeries(self.__dispatcher__)
        self.search = GetSearch(self.__dispatcher__)
    
    def __dispatcher__(self, key, *args, **kwargs):
        value = self._parser._exec_mapping(key, *args, **kwargs)
        return value
    
    @dispatched("match")
    def match(self, url) -> Dict[str, str]: ...
    
    @dispatched("images")
    def images(self, **kwargs) -> List[str]: ...