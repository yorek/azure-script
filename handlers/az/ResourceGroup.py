from handlers.Handler import Handler
from handlers.az.Generic import GenericHandler

class ResourceGroupHandler(GenericHandler):
    azure_object = "resource group"
 
    def create(self, objects, name, params):
        if not "location" in params:
            params.append(["location", self.context["location"]])

        cmd = GenericHandler.create(self, ["group"], name, params)

        self.set_context_value(objects, name)

        return cmd
 
  