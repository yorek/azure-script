from .Generic import GenericHandler

class FunctionAppHandler(GenericHandler):
    azure_object = "functionapp"
    
    def execute(self):
        fqn = self.get_full_resource_name()
        
        self.add_context_parameter("resource-group", "group")
        
        if fqn == "functionapp" and self.action == "create":

            # if no plan is specificied as parameter or available in the context
            # then assume that a consumption plan should be used
            if 'plan' not in self.params and 'appservice plan' not in self.context:
                self.add_context_parameter("consumption-plan-location", "location")
            else:
                self.add_context_parameter("plan", "appservice plan")

            self.add_context_parameter("storage-account", "storage account")

        if self.action != "create":
           self.derive_name_from_context("functionapp")    

        cmd = super(FunctionAppHandler, self).execute()

        self.save_to_context()

        return cmd

