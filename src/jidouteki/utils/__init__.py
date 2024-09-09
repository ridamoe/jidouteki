import inspect

def get(dict, path: str):
    current = dict
    for prop in path.split("."):
        if prop.isdigit():
            prop = int(prop)
        try:
            current = current[prop]
        except:
            raise KeyError(f"Cannot get property {path} from {dict} object")
    return current