import sys
from handlers.Handler import Handler

class ContextParameter:
    name = None
    context = None

    def __init__(self, name, context):
        self.name = name
        self.context = context

    def __eq__(self, other):
        if isinstance(other, ContextParameter):
            return self.name == other.name
                
        return self.name == str(other)
    
    def __str__(self):
        return "{0} => {1}".format(self.name, self.context)

class GenericHandler(Handler):
    azure_object = "*"

    context_parameters = []

    def execute(self, objects, name, params):
        cmd = u"az"
        cmd += u" {0}".format(' '.join(objects))
        cmd += u" --name {0}".format(name)

        #print("-> {0} {1}".format(objects, name))

        for cp in self.context_parameters:
            self._param_from_context(params, cp.name, cp.context)            
        
        if (len(params)>0):
            for param in params:
                cmd += u" --{0} {1}".format(param, params[param])

        return cmd
 
    def _param_from_context(self, params, param_name, context_name):
        if not param_name in params:
            if context_name in self.context:
                if context_name in self.context_parameters:
                    params[param_name] = self.context[context_name]
            else:                    
                #print("-> CONTEXT: {0}".format(self.context))
                #print("-> PARAM_CONTEXT: {0}".format(self.context_parameters))
                sys.exit("Missing '{0}' parameter and not suitable context value '{1}' found.".format(param_name, context_name))