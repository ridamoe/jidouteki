from ..parser import WebsiteParser
from ..objects import *
from .dispatcher import *

class ParamsSeries(Dispatcher):
    @property
    @dispatched("series.title")
    def title(self) -> list[str]: ...
    
    @property
    @dispatched("series.chapters")
    def chapters(self) -> list[str]: ...
    
    @property
    @dispatched("series.cover")
    def cover(self) -> list[str]: ...

class ParamsSearch(Dispatcher):
    pass
    
class ProviderParams(Dispatcher):
    def __init__(self, parser: WebsiteParser) -> None:
        self._parser = parser
        self.series = ParamsSeries(self.__dispatcher__)
        self.search = ParamsSearch(self.__dispatcher__)
    
    def __dispatcher__(self, key, *args, **kwargs):
        value = self._parser._get_mapping_params(key)
        return value
    
    @property
    @dispatched("match")
    def match(self) -> list[str]: ...
    
    @property
    @dispatched("images")
    def images(self) -> list[str]: ...