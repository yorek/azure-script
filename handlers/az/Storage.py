from handlers.Handler import Handler

class StorageShareHandler(Handler):
    azure_object = "storage share"
 
    def create(self, objects, name, params):
        cmd = "az"
        cmd += u" {0} create".format(' '.join(objects))
        cmd += u" -g {0} -n {1}".format(self.context["resource-group"], name)
        for param in params:
            cmd += " --{0} {1}".format(param[0], param[1])

        if not "account-name" in params:
            if self.context.has_key("storage-account"):
                cmd += u" --account-name {0}".format(self.context["storage-account"])
            else:    
                print("***** MISSING 'account-name' option in command")
                exit

        return cmd
    

class StorageHandler(Handler):
    azure_object = "storage"
 
    def create(self, objects, name, params):
        cmd = "az"
        cmd += u" {0} create".format(' '.join(objects))
        cmd += u" -g {0} -n {1}".format(self.context["resource-group"], name)
        cmd += u" -l {0}".format(self.context["location"])
        if (len(params)>0):
            for param in params:
                cmd += " --{0} {1}".format(param[0], param[1])
        return cmd
 
    def execute(self, objects, name, params):
        cmd = u"az"

        cmd += " {0}".format(' '.join(objects))                    

        for param in params.children:
            cmd += " --{0} {1}".format(param[0], param[1])

        print(cmd)

        
        
        