from azsc.handlers.Handler import Handler
from azsc.handlers.az.Generic import GenericHandler

class FunctionAppHandler(GenericHandler):
    azure_object = "functionapp"
    
    def execute(self):
        fqn = self.get_full_resource_name()
        
        if fqn == "functionapp":
            self.add_context_parameter("resource-group", "group")
            self.add_context_parameter("plan", "appservice plan")
            self.add_context_parameter("storage-account", "storage account")

        if fqn == "functionapp config appsettings":
            self.add_context_parameter("resource-group", "group")

        if fqn == "functionapp deployment source":            
            self.add_context_parameter("resource-group", "group")

        cmd = super(FunctionAppHandler, self).execute()

        self.save_to_context()

        return cmd

