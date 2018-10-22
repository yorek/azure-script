import sys
import collections
from azsc.handlers.Handler import Handler

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

    context_parameters = None

    def __init__(self, context, resources, action, name, params):
        super(GenericHandler, self).__init__(context, resources, action, name, params)
        self.context_parameters = []

    def execute(self):
        cmd = u"az"
        cmd += u" {0}".format(' '.join(self.resources))
        cmd += u" {0}".format(self.action)
        
        if (self.name != None):
            cmd += u" --name {0}".format(self.name)

        #print("-> {0} {1} {2}".format(self.resources, self.action, self.name))
        #print("-> CONTEXT: {0}".format(self.context))
        #print("-> PARAM_CONTEXT: {0}".format(self.context_parameters))

        for cp in self.context_parameters:
            self._param_from_context(cp.name, cp.context)            
        
        if (len(self.params)>0):
            ordered_params = collections.OrderedDict(sorted(self.params.items()))
            for param in ordered_params:
                cmd += u" --{0} {1}".format(param, self.params[param])

        return cmd
 
    def add_context_parameter(self, parameter_name, context_name):
        self.context_parameters.append(ContextParameter(parameter_name, context_name))
        
    def _param_from_context(self, param_name, context_name):
        if not param_name in self.params:
            if context_name in self.context:
                self.params[param_name] = self.context[context_name]
            else:                    
                print("-> CONTEXT: {0}".format(self.context))
                print("-> PARAM_CONTEXT: {0}".format(self.context_parameters))
                sys.exit("Missing '{0}' parameter and not suitable context value '{1}' found.".format(param_name, context_name))

    