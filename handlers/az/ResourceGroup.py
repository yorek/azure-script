from handlers.Handler import Handler

class ResourceGroupHandler(Handler):
    azure_object = "resource group"
 
    def create(self, items):
        cmd = "az"
        cmd += u" group create -n {0}".format(items[2])
        cmd += u" -l {0}".format(self.context["location"])
        return cmd
 
    def select(self, items):
        pass

    def use(self, items):
        pass