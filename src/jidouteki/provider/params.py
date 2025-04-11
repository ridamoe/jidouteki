from ..config import ProviderConfig
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
    def __init__(self, config: ProviderConfig) -> None:
        self._config = config
        self.series = ParamsSeries(self.__dispatcher__)
        self.search = ParamsSearch(self.__dispatcher__)
    
    def __dispatcher__(self, key, *args, **kwargs):
        value = self._config._get_mapping_params(key)
        return value
    
    @property
    @dispatched("match")
    def match(self) -> list[str]: ...
    
    @property
    @dispatched("images")
    def images(self) -> list[str]: ...