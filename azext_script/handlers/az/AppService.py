from azext_script.handlers.Handler import Handler
from azext_script.handlers.az.Generic import GenericHandler

class AppServiceHandler(GenericHandler):
    azure_object = "appservice"
 
    def execute(self):
        self.add_context_parameter("resource-group", "group")

        cmd = super(AppServiceHandler, self).execute()

        self.save_to_context()

        return cmd
        