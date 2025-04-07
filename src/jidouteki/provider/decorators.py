def mapping_factory(prop):
    """Add a mapping to a config class"""
    def decorator(func):
        if hasattr(func, "__mapping"):
            raise Exception(f"Duplicate funcion mapping. Remove one of @jidouteki.{prop}")
        func.__mapping = prop
        return func
    return decorator

meta = mapping_factory("meta")
match = mapping_factory("match")

class Series():
    title = staticmethod(mapping_factory("series.title"))
    chapters = staticmethod(mapping_factory("series.chapters"))
    cover = staticmethod(mapping_factory("series.cover"))
series = Series()

images = mapping_factory("images")

__all__ = ["meta", "match", "series", "images"]