from handlers.Handler import Handler
from handlers.az.Generic import GenericHandler

class ResourceGroupHandler(GenericHandler):
    azure_object = "resource group"
 
    def execute(self, objects, name, params):
        if not "location" in params:
            params["location"] = self.context["location"]

        cmd = GenericHandler.execute(self, ["group", "create"], name, params)

        self.set_context_value(objects, name)

        return cmd
 
  