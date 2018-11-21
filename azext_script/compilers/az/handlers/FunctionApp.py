from .Generic import GenericHandler

class FunctionAppHandler(GenericHandler):
    azure_object = "functionapp"
    
    def execute(self):
        fqn = self.get_full_resource_name()
        
        self.add_context_parameter("resource-group", "group")
        
        if fqn == "functionapp" and self.action == "create":
            self.add_context_parameter("plan", "appservice plan")
            self.add_context_parameter("storage-account", "storage account")

        if fqn == "functionapp deployment source" and self.action == "config-zip":
            self.add_context_parameter("name", "functionapp")    

        cmd = super(FunctionAppHandler, self).execute()

        self.save_to_context()

        return cmd

