from __future__ import absolute_import

from lark import Transformer, Tree
from lark.lexer import Token
from azext_script.compilers.HandlerManager import HandlerManager

class ScriptTransformer(Transformer):
    __handler_manager = None
    __cmd = u""
    __result = u""
    __assign_to = None
    __inner_command = None
    __target = "az"

    def  __init__(self, target):
        self.__target = target
        self.__handler_manager = HandlerManager(target)

    def __get_name_objects_params(self, items):
        name = None
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

        # Dirty trink needs to be changed to a better way
        # By using abstract methods and return a Class instead!
        if (type(result) is tuple):
            self.__inner_command = result[1]
            result = result[0]                    

        self.__cmd += result

    def variable(self, items):        
        self.__assign_to = items[0]

    def instruction(self, items):    
        if self.__assign_to is not None:
            ## Horrible, need to find a better way!
            self.__cmd = self.__cmd.replace(" -o json >> azcli-execution.log", "")            
            self.__cmd = "export {0}=$({1} -o tsv)".format(self.__assign_to, self.__cmd)

        if (self.__target == "azsh"):
            if (self.__inner_command is not None):
                self.__result += "echo '{0}: {1} {2}'".format(self.__inner_command.action, self.__inner_command.get_full_resource_name(), self.__inner_command.name or '') + "\n"           

        if (self.__cmd != ''):
            self.__result += self.__cmd + "\n\n"

        self.__cmd = u""
        self.__assign_to = None
        self.__inner_command = None

    def start(self, items):
        header = """
#!/bin/bash
set -e

if ! command az >/dev/null; then
    echo "Must install Azure CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" >&2
    exit 1
fi

on_error() {
    set +e
    echo "There was an error, execution halted" >&2
    exit 1
}

trap on_error ERR

rm azcli-execution.log -f

        \n"""

        if self.__target == "azsh":
            self.__result = header + self.__result

    def get_result(self):
        return self.__result.strip()

    def get_context(self):
        return self.__handler_manager.context