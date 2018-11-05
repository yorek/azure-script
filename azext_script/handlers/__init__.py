from azext_script.handlers.Handler import *
from importlib import import_module

import_module('azext_script.compilers.az.handlers')

def all_subclasses(cls):
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_subclasses(c)])

# find all hanlders (classes derived from Handler)
available_handlers = all_subclasses(Handler)

__all__ = ['Handler']

