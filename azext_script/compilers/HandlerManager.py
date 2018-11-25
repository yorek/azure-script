from knack.log import get_logger
from azext_script.compilers import Handler
from azext_script.compilers.Compiler import get_supported_target

logger = get_logger(__name__)

class HandlerManager:
    target = None
    context = {}
    __handlers = {}
    __available_handlers = set()

    def __get_all_subclasses(self, cls):
        return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in self.__get_all_subclasses(c)])

    def __init__(self, target):       
        self.target = target
        self.load_handlers()        

    def load_handlers(self):
        logger.debug("Registering Handlers")
        compiler = get_supported_target(self.target)
        #print('azext_script.compilers.{0}.handlers'.format(compiler))
        __import__('azext_script.compilers.{0}.handlers'.format(compiler))
        __available_handlers = self.__get_all_subclasses(Handler)
        for h in __available_handlers:
            logger.debug("Found Handler: '{0}'".format(h.azure_object))
            if h.azure_object in self.__handlers:
                error_message = "Duplicate Handler found: '{0}'".format(h.azure_object) 
                logger.error(error_message)
                raise RuntimeError(error_message)
            self.__handlers[h.azure_object] = h        

    def set_context(self, name, value):        
        self.context[name] = value

    def is_handler_available(self, azobject): 
        return azobject in self.__handlers

    def get_handler(self, resources, action, name, params):
        fqn = ''

        # check what is the most specific handler possible        
        for i in range(len(resources), 0, -1):
            fqn = ' '.join(resources[0:i])
            if self.is_handler_available(fqn):
                break

        h = None

        # if an handler is found use it otherwise fall back
        # to the generic handler
        if self.is_handler_available(fqn):
            h = self.__handlers[fqn]
        else:
            h = self.__handlers["*"]

        return h(self.context, resources, action, name, params, self.target)
