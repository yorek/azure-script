from handlers.Handler import Handler
from handlers.az.Generic import GenericHandler

class AppServiceHandler(GenericHandler):
    azure_object = "appservice"
 
    def execute(self):
        self.add_context_parameter("resource-group", "group")

        cmd = super().execute()

        self.save_to_context()

        return cmd
        