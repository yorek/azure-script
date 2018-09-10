from Handler import Handler

class StorageHandler(Handler):
    azure_object = "storage"
 
    def create(self, items):
        cmd = "az"
        cmd += u" storage create {0}".format(items[1])
        cmd += u" -g {0} -n {1}".format(self.context["resource-group"], items[2])
        cmd += u" -l {0}".format(self.context["location"])
        if (len(items)>3):
            for param in items[3].children:
                cmd += " --{0} {1}".format(param[0], param[1])
        return cmd
 
    def select(self, items):
        pass

    def use(self, items):
        pass


        
        
        