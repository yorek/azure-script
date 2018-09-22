from handlers.Handler import Handler

class ResourceGroupHandler(Handler):
    azure_object = "resource group"
 
    def create(self, objects, name, params):
        cmd = "az"
        cmd += u" group create -n {0}".format(name)
        cmd += u" -l {0}".format(self.context["location"])

        self.set_context_value(objects, name)

        return cmd
 
  