import types

def simple_make_picklable(obj):
    """
Convert an object into a picklable object, by converting everything that is not a basic data type (None, boolean, int, float, complex, str, bytes, bytearrays) or basic data structure (tuple, list, set, dict) into strings.
Additionally, range and generator objects will be converted to lists.

Parameter(s):
- obj: Object to be converted

Returns: Picklable object
    """

    if obj is None: return None
    
    if isinstance(obj, (bool, int, float, complex, str, bytes, bytearray)): return obj

    if isinstance(obj, tuple):
        return tuple((simple_make_picklable(i) for i in obj))

    if isinstance(obj, list):
        return [simple_make_picklable(i) for i in obj]
    
    if isinstance(obj, set):
        return {simple_make_picklable(i) for i in obj}
    
    if isinstance(obj, dict):
        return {i: simple_make_picklable(obj[i]) for i in obj}
    
    if isinstance(obj, range):
        return list(obj)
    
    if isinstance(obj, types.GeneratorType):
        return [simple_make_picklable(i) for i in list(obj)]

    return str(obj)