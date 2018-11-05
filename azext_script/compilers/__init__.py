import pkgutil 
from azext_script.compilers.Handler import *
from importlib import import_module

__path__ = pkgutil.extend_path(__path__, __name__)
for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__+'.'):
    __import__(modname)
    


