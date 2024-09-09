import re
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urljoin
import itertools
import requests
import json
from functools import reduce
import urllib.parse

@dataclass
class Metadata():
    key: str 
    display_name: str
    base: str = field(default=None)
    languages: list = field(default=None)

@dataclass
class Chapter():
    params: Dict[str, str]
    volume: str
    chapter: str 
    title: str
    language: str

import typing
if typing.TYPE_CHECKING:
    from .. import Jidouteki

class FetchType(Enum):
    REQUEST = 1 
    NETWORK = 2 
    
from bs4 import BeautifulSoup

class FetchedData():
    def __init__(self, data, type) -> None:
        self._index = 0
        self._data = data if isinstance(data, (list,tuple)) else [data]
        self.type = type
    
    def __iter__(self):
        for i in range(0, len(self._data)):
            self._index = i
            yield self
        self._index = 0
    
    @property
    def data(self):
        return self._data[self._index]
    
    def json(self):
        return json.loads(self.data)

    def css(self, query):
        soup = BeautifulSoup(self.data, features="lxml")
        return soup.select(query)
    
    def css(self, query):
        soup = BeautifulSoup(self.data, features="lxml")
        return soup.select(query)
    
    def regex(self, query):
        return re.findall(query, self.data)
    
    def xpath(self, query):
        raise NotImplementedError()

from typeguard import check_type
import inspect
import time

class Config():
    __MAPPINGS: dict
    __MAPPINGS_TYPES = {
        "meta": Metadata,
        "match": List[str] | Tuple[str, ...],
        "series.chapters": List[Chapter],
        "series.title": str,
        "series.cover": str,
        "images": List[str],
    }
    __MAPPINGS_REQUIRED = ["meta", "images"]
    
    def __init__(self, _context: "Jidouteki") -> None:
        self._context = _context
    
    def __init_subclass__(cls, **kwargs):
        cls.__MAPPINGS = {}
        for obj in vars(cls).values():
            mapping =  getattr(obj, "__mapping", None)
            if mapping:
                cls.__MAPPINGS[mapping] = obj

    def __get(self, key):
        return self.__MAPPINGS.get(key)
    
    def has(self, key):
        """
        Checks if a config method is availablbe
            
            Example: `config.has("series.chapter")` will return True / False
            based on whether the config supports chapter lists
        """
        return self.__get(key) != None
    
    
    def params(self, key):
        """Returns the parameters of the config method
            
            Example: `config.params("series.chapter")` returns the list
            of keyword parameters for `config.series.chapter()`
        """
        func = self.__get(key)
        if func:
            signature = inspect.signature(func)
            args = [
                param.name for param in signature.parameters.values()
            ]
            return args[1:]
        else: return []
    
    def _get(self, key, **kwargs):
        func = self.__get(key)
        if not func: 
            if  key in self.__MAPPINGS_REQUIRED:
                raise Exception(f"Missing @jidouteki.{key} from {self.__class__.__name__}")
            else: return None
        
        params  =self.params(key)
        kwargs  = {key: value for key,value in kwargs.items() if key in params} 
        value = func(self, **kwargs)
        type = self.__MAPPINGS_TYPES.get(key, None)
        if type:
            try:
                check_type(value, type)
            except Exception as e:
                file_path = inspect.getfile(func)
                source_lines, line_number = inspect.getsourcelines(func)
                function_name = func.__name__
                
                # Format the output
                e.add_note(f"  File \"{file_path}\", line {line_number}, in {function_name}\nType check failed for @jidouteki.{key}. Check your return type")
                raise e

        return value
    
    def fetch(self, *args, type=FetchType.REQUEST) -> FetchedData:
        if self.meta.base: args = (self.meta.base, *args) 
        def _fetch(args, type):
            if type == FetchType.REQUEST:
                args = [arg if isinstance(arg, (list,tuple)) else [arg] for arg in args]
                urls = [reduce(lambda a, b: urljoin(a, b), p) for p in itertools.product(*args)]
                
                contents = []
                for url in urls:
                    resp = requests.get(url)
                    if not resp.ok: continue
                    contents.append(resp.content)
                return FetchedData(contents, type)
        
        cache = self._context.cache
        cache_key = hash(str((*args, type)))

        if cache_key in cache.keys():
            cache_hit = cache[cache_key]
            if time.time() - cache_hit[1] <= cache_hit[2]:
                 return cache_hit[0]
        
        value = _fetch(args, type)
        cache[cache_key] = (value, time.time(), self._context.cache_ttl)
        return cache[cache_key][0]
        
    def proxy(self, url, headers: Dict[str, str]={}):
        params = []
        for key,val in headers.items():
            header = ''.join([w.capitalize() for w in key.split('-')])
            params.append(('header', f"{header}: {val}"))
    
        params.append(("url", url))
        query_string = urllib.parse.urlencode(params)
            
        return f"{self._context.proxy}?{query_string}"
            
    class Series:
        def __init__(self, config: "Config"):
            self.config = config

        def title(self, **kwargs) -> str:
            return self.config._get("series.title", **kwargs)

        def chapters(self, **kwargs) -> List[Chapter]:
            return self.config._get("series.chapters", **kwargs)

        def cover(self, **kwargs) -> str:
            return self.config._get("series.cover", **kwargs)

    @property
    def series(self):
        return Config.Series(self)
    
    @property
    def meta(self) -> Metadata:
        return self._get("meta")

    def match(self, url):
        patterns = self._get("match")
        for pattern in patterns:
            if (m := re.match(pattern, url)):
                return m.groupdict()
        return None
        
    def images(self, **kwargs) -> List[str]:
        return self._get("images", **kwargs)

    class Search:
        def __init__(self, config: "Config"):
            self.config = config

    @property
    def search(self):
        return Config.Search(self)