from handlers.Handler import Handler

class GenericHandler(Handler):
    azure_object = "*"

    def create(self, objects, name, params):
        cmd = u"az"
        cmd += u" {0} create".format(' '.join(objects))
        cmd += u" --name {0}".format(name)
        
        if (len(params)>0):
            for param in params:
                cmd += u" --{0} {1}".format(param[0], param[1])

        cmd += u" -o table"

        return cmd
 
