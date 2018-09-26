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
 
