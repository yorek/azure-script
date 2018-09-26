import logging
from handlers import available_handlers
from handlers import Handler

class HandlerManager:
    context = {}
    __handlers = {}

    def __init__(self):
        self.load_handlers()        

    def load_handlers(self):
        logging.info("registering handlers")
        for h in available_handlers:
            logging.debug("\tfound handler: '{0}'".format(h.azure_object))
            self.__handlers[h.azure_object] = h(self.context)
        print

    def set_context(self, name, value):
        self.context[name] = value

    def is_handler_available(self, azobject): 
        return azobject in self.__handlers

    def get_handler(self, azobjects):
        fqn = ''

        for i in range(len(azobjects), 0, -1):
            fqn = ' '.join(azobjects[0:i])
            if self.is_handler_available(fqn):
                break

        if self.is_handler_available(fqn):
            return self.__handlers[fqn]
        else:
            return self.__handlers["*"]
