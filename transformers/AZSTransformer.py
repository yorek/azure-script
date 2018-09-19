from lark import Transformer, Tree
from lark.lexer import Token
from handlers.HandlerManager import HandlerManager

class AZSTransformer(Transformer):
    __handler_manager = HandlerManager()

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
        if len(items) == 2:
            k = items[0]
            v = items[1]

        if len(items) == 3:
            k = "{0}-{1}".format(items[0], items[1])
            v = items[2]

        #print("[set {0} = {1}]".format(k, v))
        self.__handler_manager.set_context(k, v)

    def create(self, items):                
        cmd = u""
        
        objects = []
        params = []
        for item in items:
            if isinstance(item, Token) and item.type == 'OBJECT':
                objects.append(str(item))
            elif isinstance(item, Tree):
                params = item.children
            else:
                name = str(item)

        fqon = ''

        for i in range(len(objects), 0, -1):
            fqon = ' '.join(objects[0:i])
            if self.__handler_manager.is_handler_available(fqon):
                break

        if self.__handler_manager.is_handler_available(fqon):
            handler = self.__handler_manager.get_handler(fqon)
            cmd += handler.create(objects, name, params)            
        else:
            print("***** MISSING HANDLER FOR: '{0}'".format(fqon))             

        print(cmd)

    def execute(self, items):
        cmd = u"az"

        cmd += " {0} {1}".format(items[0], items[1])                    

        params = [i for i in items if isinstance(i, Tree)][0]

        for param in params.children:
            cmd += " --{0} {1}".format(param[0], param[1])

        print(cmd)

    def instruction(self, items):    
        pass