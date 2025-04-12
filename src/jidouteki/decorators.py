from .exceptions import *
from typing import Tuple, Dict, Any

def make_map_decorator(key):
    def decorator(func):
        if hasattr(func, "__mapping"):
            raise DuplicatedMappingDecoratorError("Functions can have at most one mapping decorator")
        func.__mapping = key
        return func
    return decorator

class MapDecorators:
    def __init__(self):
        self.series = MapDecorators.SeriesDecorators()
        self.images = make_map_decorator("images")
        self.match = make_map_decorator("match")
    
    class SeriesDecorators:
        def __init__(self):
            self.title = make_map_decorator("series.title")
            self.chapters = make_map_decorator("series.chapters")
            self.cover = make_map_decorator("series.cover")
        
map = MapDecorators()

from .tests import TestKind, Test

def test(input: Tuple[Any] | Dict | Any, expected_output: Dict=None, kind: TestKind = None):
    def method(func):
        if hasattr(func, "__mapping"):
            if not hasattr(func, "__tests"):
                func.__tests = []
            func.__tests.append(Test(input, expected_output, kind))
        else:
            TestWithoutMappingError("Cannot decorate a test without a mapping. Try calling one of `@jidouteki.map.*` first")
        return func
    return method