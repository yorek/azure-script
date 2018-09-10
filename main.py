import sys
from lark import Lark, Transformer
from handlers import HandlerManager

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
        
        obj = items[0]

        if (items[1].type == 'OBJECT'):
            obj2 = obj + " " + items[1]
            if self.__handler_manager.is_handler_available(obj2):
                obj = obj2
        
        #print("***** FOUND OBJECT: '{0}'".format(obj))

        if self.__handler_manager.is_handler_available(obj):
            handler = self.__handler_manager.get_handler(obj)
            cmd += handler.create(items)            
        else:
            print("***** MISSING HANDLER FOR: '{0}'".format(obj))
     
        # if (obj.startswith("eventgrid topic")):
        #     cmd += u" eventgrid topic create -g {0} -n {1}".format(self.context["resource-group"], items[2])
        #     cmd += u" -l {0}".format(self.context["location"])

        # if (obj.startswith("storage")):
        #     cmd += u" storage create {0}".format(items[1])
        #     cmd += u" -g {0} -n {1}".format(self.context["resource-group"], items[2])
        #     cmd += u" -l {0}".format(self.context["location"])
        #     if (len(items)>3):
        #         for param in items[3].children:
        #             cmd += " --{0} {1}".format(param[0], param[1])

        print(cmd)

    def execute(self, items):
        cmd = u"az"

        cmd += " {0} {1}".format(items[0], items[1])

        for param in items[2].children:
            cmd += " --{0} {1}".format(param[0], param[1])

        print(cmd)

    def instruction(self, items):    
        pass


def main(debug=0):
    print('loading grammar...')
    with open('aql2.lark', 'r') as f:
        aql_grammar = f.read()

    print('loading adl file...')
    with open('test3.adl', 'r') as f:
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

if __name__ == '__main__':

    if ( len(sys.argv) == 1 ):
        main()
    
    if ( len(sys.argv) == 2 and sys.argv[1] == "debug" ):   
        main(1)