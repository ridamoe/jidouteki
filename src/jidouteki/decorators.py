from .exceptions import *

def make_map_decorator(key):
    def decorator(func):
        if hasattr(func, "__mapping"):
            raise DuplicatedMappingDecorator("Functions can have at most one mapping decorator")
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