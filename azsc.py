import sys
from lark import Lark, Transformer, Tree
from lark.lexer import Token
from handlers.HandlerManager import HandlerManager

class AQLTransformer(Transformer):
    __handler_manager = HandlerManager()

    def pair(self, (k,v)):
        return k,v

    def action(self, (s,)):
        return s[1:-1]

    def azvalue(self, (s,)):
        return s

    def string(self, (s,)):
        return '"' + s[1:-1] + '"'

    def azname(self, (s,)):
        return '"' + s[1:-1] + '"'

    def azobject(self, (s,)):
        return s

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


def main(adl_file, debug=False):
    print('loading grammar...')
    with open('aql-b.lark', 'r') as f:
        aql_grammar = f.read()

    print('loading adl file...')
    with open(adl_file, 'r') as f:
        text = f.read()

    print('parsing...')
    parser = Lark(aql_grammar)
    tree = parser.parse(text)

    if (debug):
        print('resulting parse tree')
        print(tree.pretty())
        print

    print('transpilation results:')
    print
        
    AQLTransformer().transform(tree)    
    print

def show_help():
    print("aldc <file.adl> [options]")
    print
    print("options:")
    print(" --debug : print debug info")


if __name__ == '__main__':
    debug = False

    if ( len(sys.argv) < 2 or len(sys.argv) > 3 ):
        show_help()
        exit
    
    if ( len(sys.argv) == 3):   
        if sys.argv[2].lower() == "--debug":
            debug = True                

    main(sys.argv[1], debug)