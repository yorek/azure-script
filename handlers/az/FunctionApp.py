from handlers.Handler import Handler
from handlers.az.Generic import GenericHandler

class FunctionAppHandler(GenericHandler):
    azure_object = "functionapp"
    
    def execute(self):
        fqn = self.get_full_resource_name()
        
        if fqn == "functionapp":
            self.add_context_parameter("resource-group", "group")
            self.add_context_parameter("plan", "appservice plan")
            self.add_context_parameter("storage-account", "storage account")

        if fqn == "functionapp config":
            self.add_context_parameter("resource-group", "group")

        if fqn == "functionapp deployment":
            self.add_context_parameter("plan", "appservice plan")
            self.add_context_parameter("resource-group", "group")

        if fqn == "eventhubs namespace authorization-rule keys list":
            self.add_context_parameter("namespace-name", "eventhubs namespace")
            self.add_context_parameter("resource-group", "group")

        if fqn == "eventhubs namespace":
            self.add_context_parameter("resource-group", "group")
            self.add_context_parameter("location", "location")

        cmd = super(FunctionAppHandler, self).execute()

        self.save_to_context()

        return cmd

