from ..parser import WebsiteParser
from ..objects import *
from .dispatcher import *
from ..tests import TestsOutcome

class TestSeries(Dispatcher):
    @dispatched("series.title")
    def title(self) -> bool: ...
    
    @dispatched("series.chapters")
    def chapters(self) -> bool: ...
    
    @dispatched("series.cover")
    def cover(self) -> bool: ...

class TestSearch(Dispatcher):
    pass
    
class ProviderTest(Dispatcher):
    def __init__(self, parser: WebsiteParser) -> None:
        self._parser = parser
        self.series = TestSeries(self.__dispatcher__)
        self.search = TestSearch(self.__dispatcher__)
    
    def __dispatcher__(self, key, *args, **kwargs) -> TestsOutcome:
        outcome = TestsOutcome()
        for test in self._parser._get_tests(key):
            def test_runner(*args, **kwargs):
                return self._parser._exec_mapping(key, *args, **kwargs)
            output = test.run(test_runner)
            outcome.append(output)
        return outcome
    
    def all(self) -> Dict[str, bool]:
        state = {}
        for key in self._parser._get_keys():            
            outcome = self.__dispatcher__(key)
            keys = key.split(".")
            d = state
            for key in keys[:-1]:
                d = d.setdefault(key, {})
            d[keys[-1]] = outcome
        return state
    
    @dispatched("match")
    def match(self) -> bool: ...
    
    @dispatched("images")
    def images(self) -> bool: ...