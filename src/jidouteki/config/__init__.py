from requests_cache import CachedSession
from typing import Dict, List, Callable
from urllib.parse import urljoin
import itertools
from functools import reduce
import urllib.parse
from abc import ABC, abstractmethod
from ..objects import Metadata
from .fetch import FetchedData
from ..tests import Test
from ..exceptions import *
import typing
import inspect
if typing.TYPE_CHECKING:
    from .. import Jidouteki

MAPPINGS_REQUIRED = ["images"]
    
class ProviderConfig(ABC):
    """
    The configuration for a single scraper. Each website should extend 
    this class and it will automatically get loaded by jidouteki.
    """
    
    @property
    @abstractmethod
    def meta(self) -> Metadata:
        pass
        
    __MAPPINGS: Dict[str, Callable]
    __TESTS: Dict[str, List[Test]]

    def __init__(self, context: "Jidouteki") -> None:
        self.context = context
        self.session = CachedSession(expire_after=self.context.cache_ttl, backend="memory")
        
    def __init_subclass__(cls, **kwargs):
        cls.__MAPPINGS = {}
        cls.__TESTS = {}
        for obj in vars(cls).values():
            mapping =  getattr(obj, "__mapping", None)
            tests =  getattr(obj, "__tests", None)
            if mapping:
                cls.__MAPPINGS[mapping] = obj
                cls.__TESTS[mapping] = tests
        for key in MAPPINGS_REQUIRED:
            if key not in cls.__MAPPINGS:
                raise MissingRequiredMappingError(f"Missing @jidouteki.{key} from {self.__class__.__name__}")
    
    def _get_keys(self):
        return list(self.__MAPPINGS.keys())
    
    def _get_mapping(self, key, required=False):
        value = self.__MAPPINGS.get(key)
        if value is None and required:
            raise MissingMappingError(f"Missing mapping '{key}' from {self.__class__.__name__}")
        return value
    
    def _get_tests(self, key, required=False):
        value = self.__TESTS.get(key)
        if value is None:
            if required:
                raise MissingTestError(f"Missing test for mapping '{key}' from {self.__class__.__name__}")
            else: value = []
        return value
    
    def _get_mapping_params(self, key):
        """Returns the parameters of the mapping"""
        func = self._get_mapping(key, required=True)
        signature = inspect.signature(func)
        args = [
            param.name for param in signature.parameters.values()
        ]
        return args[1:]
    
    def _exec_mapping(self, key, *args, **kwargs):
        mapping = self._get_mapping(key, required=True)
        signature = inspect.signature(mapping)
        
        # Filter arguments, ignoring eventual extra parameters
        max_args = sum(1 for p in signature.parameters.values()
                if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD))
        
        filtered_args = [self, *args][:max_args]
        filtered_kwargs = {
            k: v for k, v in kwargs.items()
            if k in signature.parameters.keys()
        }
        
        # Match arguments to function signature parameters
        try:
            bound = signature.bind(*filtered_args, **filtered_kwargs)
        except TypeError as e:
            raise MappingWrongArgumentsError(f"Wrong arguments '{mapping.__qualname__}' {str(e)}")
        bound.apply_defaults()
        return mapping(*bound.args, **bound.kwargs)
        
    @property
    def provider(self): 
        from ..provider.provider import Provider
        return Provider(self)
    
    def fetch(self, *args, method="GET", **kwargs) -> FetchedData:
        if self.meta.base: args = (self.meta.base, *args) 
        args = [arg if isinstance(arg, (list,tuple)) else [arg] for arg in args]
        urls = [reduce(lambda a, b: urljoin(a, b), p) for p in itertools.product(*args)]
        
        contents = []
        for url in urls:
            resp = self.session.request(method, url, **kwargs)
            if not resp.ok: continue
            contents.append(resp.content)
        return FetchedData(contents)


    def proxy(self, url, headers: Dict[str, str]={}):
        params = []
        for key,val in headers.items():
            header = ''.join([w.capitalize() for w in key.split('-')])
            params.append(('header', f"{header}: {val}"))
    
        params.append(("url", url))
        query_string = urllib.parse.urlencode(params)
            
        return f"{self.context.proxy}?{query_string}"