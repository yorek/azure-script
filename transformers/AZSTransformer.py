from lark import Transformer, Tree
from lark.lexer import Token
from handlers.HandlerManager import HandlerManager

class AZSTransformer(Transformer):
    __handler_manager = HandlerManager()
    __cmd = u""

    def __get_name_objects_params(self, items):
        objects = []
        params = []
        for item in items:
            if isinstance(item, Token) and item.type == 'OBJECT':
                objects.append(str(item))
            elif isinstance(item, Tree):
                params = item.children
            else:
                name = str(item)

        return name, objects, params

    def pair(self, kv):
        k,v = kv
        return k,v

    def action(self, s):        
        return s[0][1:-1]

    def azvalue(self, s):
        return s[0]

    def string(self, s):
        return '"' + s[0][1:-1] + '"'

    def azname(self, s):
        return '"' + s[0][1:-1] + '"'

    def azobject(self, s):
        return s[0]

    def use(self, items):        
        k = '-'.join(items[0:-1])
        v = items[-1]
        self.__handler_manager.set_context(k, v)

    def create(self, items):                       
        name, objects, params = self.__get_name_objects_params(items)

        handler = self.__handler_manager.get_handler(objects)
        self.__cmd += handler.create(objects, name, params)            

    def execute(self, items):                
        name, objects, params = self.__get_name_objects_params(items)

        handler = self.__handler_manager.get_handler(objects)
        self.__cmd += handler.create(objects, name, params)            

    def instruction(self, items):    
        self.__cmd += "\n"

    def get_command(self):
        return self.__cmd

    def get_context(self):
        return self.__handler_manager.context