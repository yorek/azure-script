from azext_script.compilers.Handler import *
from azext_script.compilers.HandlerManager import *
from azext_script.compilers.Compiler import *

import pkgutil 

__path__ = pkgutil.extend_path(__path__, __name__)
for importer, modname, ispkg in pkgutil.walk_packages(path=__path__):
    #print('azext_script.compilers.' + modname)
    __import__('azext_script.compilers.' + modname)
