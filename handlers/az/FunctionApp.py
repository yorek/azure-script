from handlers.Handler import Handler
from handlers.az.Generic import GenericHandler

class FunctionAppConfigHandler(GenericHandler):
    azure_object = "functionapp config"
 
    def execute(self, objects, name, params):
        self._param_from_context(params, "resource-group", "resource group")

        cmd = GenericHandler.execute(self, objects, name, params)

        return cmd

class FunctionAppDeploymentHandler(GenericHandler):
    azure_object = "functionapp deployment"
 
    def execute(self, objects, name, params):
        self._param_from_context(params, "resource-group", "resource group")
        self._param_from_context(params, "plan", "appservice plan")

        cmd = GenericHandler.execute(self, objects, name, params)

        return cmd
        
class FunctionAppHandler(GenericHandler):
    azure_object = "functionapp"
 
    def execute(self, objects, name, params):
        self._param_from_context(params, "resource-group", "resource group")
        self._param_from_context(params, "plan", "appservice plan")
        self._param_from_context(params, "storage-account", "storage account")

        cmd = GenericHandler.execute(self, objects, name, params)

        self.set_context_value(objects, name)

        return cmd

