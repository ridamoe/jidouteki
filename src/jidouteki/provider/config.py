from requests_cache import CachedSession
from typing import Dict
from urllib.parse import urljoin
import itertools
from functools import reduce
import urllib.parse
from .fetch import FetchedData
import typing
if typing.TYPE_CHECKING:
    from .. import Jidouteki
    
class ProviderConfigUtils():
    def __init__(self, config: "ProviderConfig") -> None:
        self.config = config
    
    @property
    def provider(self): 
        from .provider import Provider
        return Provider(self.config)
    
    def fetch(self, *args, method="GET", **kwargs) -> FetchedData:
        if self.provider.meta.base: args = (self.provider.meta.base, *args) 
        args = [arg if isinstance(arg, (list,tuple)) else [arg] for arg in args]
        urls = [reduce(lambda a, b: urljoin(a, b), p) for p in itertools.product(*args)]
        
        contents = []
        for url in urls:
            resp = self.config.session.request(method, url, **kwargs)
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
            
        return f"{self.config.context.proxy}?{query_string}"
    
class ProviderConfig():
    """
    The configuration for a single scraper. Each website should implement 
    this class and register it with `@jidouteki.register` to get it loaded by jidouteki.
    """
    
    __MAPPINGS: dict

    def __init__(self, context: "Jidouteki") -> None:
        self.context = context
        self.session = CachedSession(expire_after=self.context.cache_ttl, backend="memory")
        self.utils = ProviderConfigUtils(self)
        
    def __init_subclass__(cls, **kwargs):
        cls.__MAPPINGS = {}
        for obj in vars(cls).values():
            mapping =  getattr(obj, "__mapping", None)
            if mapping:
                cls.__MAPPINGS[mapping] = obj
    
    def _get(self, key):
        return self.__MAPPINGS.get(key)
    