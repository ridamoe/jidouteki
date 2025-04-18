from ..parser import WebsiteParser
from ..objects import *
from .dispatcher import *

class HasSeries(Dispatcher):
    @property
    @dispatched("series.title")
    def title(self) -> bool: ...
    
    @property
    @dispatched("series.chapters")
    def chapters(self) -> bool: ...
    
    @property
    @dispatched("series.cover")
    def cover(self) -> bool: ...

class HasSearch(Dispatcher):
    pass
    
class ProviderHas(Dispatcher):
    def __init__(self, parser: WebsiteParser) -> None:
        self._parser = parser
        self.series = HasSeries(self.__dispatcher__)
        self.search = HasSearch(self.__dispatcher__)
    
    def __dispatcher__(self, key, *args, **kwargs):
        value = self._parser._get_mapping(key)
        return value is not None
    
    @property
    @dispatched("match")
    def match(self) -> bool: ...
    
    @property
    @dispatched("images")
    def images(self) -> bool: ...