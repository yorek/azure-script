from __future__ import absolute_import

from lark import Transformer, Tree
from lark.lexer import Token
from azext_script.compilers.HandlerManager import HandlerManager
from .TranspilationResult import AZCLICommand, CommandResult, ExportCommand, EmptyCommand
from knack.log import get_logger

logger = get_logger(__name__)

class ScriptTransformer(Transformer):

    __handler_manager = None
    __target = "az"

    __result = ""

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
        return EmptyCommand()

    def execute(self, items):                
        name, objects, params = self.__get_name_objects_params(items)
        resources = objects[0:-1]
        action = objects[-1]

        handler = self.__handler_manager.get_handler(resources, action, name, params)
        result = handler.execute()       

        if not isinstance(result, CommandResult):
            raise(Exception("Transpilation result is an unexpected type: {0}".format(type(result))))

        return result

    def variable(self, items):        
        return ExportCommand(items[0], None)

    def instruction(self, items):          
        if isinstance(items[0], ExportCommand):
            items[0].value = items[1]
        
        return items[0]

    def start(self, items):        
        self.__result = ""
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

"""
        logger.debug("Target: {0}".format(self.__target))

        if self.__target == "azsh":
            self.__result += header

        for i in items:            
            i.target = self.__target
            command = str(i)
            if command != "":
                self.__result += str(i)
                self.__result += "\n"
        
        self.__result += "\necho \"done\""

    def get_result(self):
        return self.__result.strip()

    def get_context(self):
        return self.__handler_manager.context