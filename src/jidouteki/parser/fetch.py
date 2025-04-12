import re
import json
from bs4 import BeautifulSoup

class FetchedData():
    def __init__(self, data) -> None:
        self._index = 0
        self._data = data if isinstance(data, (list,tuple)) else [data]
    
    def __iter__(self):
        for i in range(0, len(self._data)):
            self._index = i
            yield self
        self._index = 0
    
    @property
    def data(self):
        if self._index < len(self._data): 
            return self._data[self._index]
        else: return None
    
    def json(self):
        return json.loads(self.data)

    def css(self, query):
        soup = BeautifulSoup(self.data, features="lxml")
        return soup.select(query)
    
    def regex(self, query):
        return re.findall(query, self.data)
    
    def xpath(self, query):
        raise NotImplementedError()
