from handlers.Handler import Handler
from handlers.az.Generic import GenericHandler

class ResourceGroupHandler(GenericHandler):
    azure_object = "group"
 
    def execute(self):
        self.add_context_parameter("location", "location")

        cmd = super().execute()

        self.save_to_context()

        return cmd
 
  