import logging
from azsc.handlers import available_handlers
from azsc.handlers import Handler

class HandlerManager:
    context = {}
    __handlers = {}

    def __init__(self):
        self.load_handlers()        

    def load_handlers(self):
        logging.info("registering handlers")
        for h in available_handlers:
            logging.debug("\tfound handler: '{0}'".format(h.azure_object))
            if h.azure_object in self.__handlers:
                error_message = "duplicate handler found: '{0}'".format(h.azure_object) 
                logging.error("\t" + error_message)
                raise RuntimeError(error_message)
            self.__handlers[h.azure_object] = h
        print

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

        return h(self.context, resources, action, name, params)
