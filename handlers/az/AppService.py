from handlers.Handler import Handler
from handlers.az.Generic import GenericHandler

class AppServiceHandler(GenericHandler):
    azure_object = "appservice"
 
    def execute(self, objects, name, params):
        self._param_from_context(params, "resource-group", "resource group")

        cmd = GenericHandler.execute(self, objects, name, params)

        self.set_context_value(objects, name)

        return cmd

