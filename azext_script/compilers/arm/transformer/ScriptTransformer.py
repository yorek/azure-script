from __future__ import absolute_import

from lark import Transformer, Tree
from lark.lexer import Token
from azext_script.compilers.HandlerManager import HandlerManager

class ScriptTransformer(Transformer):
    __handler_manager = None
    __arm = u""
    __result = u""
    __assign_to = None
    __inner_command = None
    __target = "arm"

    def  __init__(self, target):
        self.__target = target
        self.__handler_manager = HandlerManager(target)

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

        params_dict = {}
        for param in params:
            params_dict[str(param[0])] = param[1]

        #print(params_dict)

        return name, objects, params_dict

    def pair(self, kv):
        k,v = kv
        return k,v

    def action(self, s):        
        return s[0][1:-1]

    def azvalue(self, s):
        return s[0]

    def string(self, s):
        return s[0][1:-1]

    def azname(self, s):
        return s[0][1:-1]

    def azfile(self, s):
        return s[0]

    def azobject(self, s):
        return s[0]

    def use(self, items):        
        k = ' '.join(items[0:-1])
        v = items[-1]
        self.__handler_manager.set_context(k, v)

    def execute(self, items):                
        name, objects, params = self.__get_name_objects_params(items)
        resources = objects[0:-1]
        action = objects[-1]

        handler = self.__handler_manager.get_handler(resources, action, name, params)
        result = handler.execute()                             

        self.__result += result

    def variable(self, items):        
        pass

    def instruction(self, items):    
        pass 

    def start(self, items):
        pass

    def get_result(self):
        return self.__result.strip()

    def get_context(self):
        return self.__handler_manager.context