from functools import wraps

class Dispatcher:
    def __dispatcher__(self, key, *args, **kwargs):
        raise NotImplementedError()
    
    def __init__(self, dispatcher=None):
        if dispatcher:
            self.__dispatcher__ = dispatcher

def dispatched(key):
    def decorator(f):
        @wraps(f)
        def new_f(self, *args, **kwargs):
            return self.__dispatcher__(key, *args, **kwargs)
        return new_f
    return decorator