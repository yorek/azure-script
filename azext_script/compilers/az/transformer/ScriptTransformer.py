from __future__ import absolute_import

from lark import Transformer, Tree
from lark.lexer import Token
from azext_script.compilers.HandlerManager import HandlerManager
from .TranspilationResult import AZCLICommand, EchoCommand, CommandResult

class ScriptTransformer(Transformer):

    __handler_manager = None
    __execute_result = None
    __assign_to = None
    __inner_command = None
    __target = "az"

    __result = u""
    __instructions = []

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

        if isinstance(result, CommandResult):
            self.__execute_result = result
        else:
            raise(Exception("Transpilation result is an unexpected type: {0}".format(type(result))))
        #self.__cmd += result

    def variable(self, items):        
        self.__assign_to = items[0]

    def instruction(self, items):            
        if self.__execute_result is None:
            return
        
        if (self.__target == "azsh"):
            src = self.__execute_result.source
            cmd = "echo '{0}: {1} {2}'".format(src.action, src.get_full_resource_name(), src.name or '')           
            self.__instructions.append(EchoCommand(cmd))

        if self.__assign_to is not None:
            self.__execute_result.assign_to = self.__assign_to
            self.__assign_to = None

        self.__instructions.append(self.__execute_result)

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

        # if self.__target == "azsh":
        #     self.__result = header + self.__result

        for i in self.__instructions:
            if (isinstance(i, AZCLICommand)):
                if i.assign_to is not None:
                    #     self.__cmd = self.__cmd.replace(" -o json >> azcli-execution.log", "")            
                    self.__result += "export {0}=$({1} -o tsv)".format(i.assign_to, i.command)
                else:
                    self.__result += i.command
                    if (self.__target == "azsh"):
                        self.__result += " -o json >> azcli-execution.log"
                    else:
                        self.__result += " -o json"
            else:
                self.__result += "\n"     
                self.__result += i.command

            self.__result += "\n"
                        
    def get_result(self):
        return self.__result.strip()

    def get_context(self):
        return self.__handler_manager.context