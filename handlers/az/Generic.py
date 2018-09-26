import sys
from handlers.Handler import Handler

class GenericHandler(Handler):
    azure_object = "*"

    def execute(self, objects, name, params):
        cmd = u"az"
        cmd += u" {0}".format(' '.join(objects))
        cmd += u" --name {0}".format(name)
        
        if (len(params)>0):
            for param in params:
                cmd += u" --{0} {1}".format(param, params[param])

        return cmd
 
    def _param_from_context(self, params, param_name, context_name):
        if not param_name in params:
            if context_name in self.context:
                params[param_name] = self.context[context_name]
            else:
                sys.exit("Missing '{0}' parameter and not suitable context value '{1}' found.".format(param_name, context_name))