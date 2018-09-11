from handlers.Handler import Handler

class StorageHandler(Handler):
    azure_object = "storage"
 
    def create(self, objects, name, params):
        cmd = "az"
        cmd += u" storage create {0}".format(objects[1])
        cmd += u" -g {0} -n {1}".format(self.context["resource-group"], name)
        cmd += u" -l {0}".format(self.context["location"])
        if (len(params)>0):
            for param in params:
                cmd += " --{0} {1}".format(param[0], param[1])
        return cmd
 


        
        
        