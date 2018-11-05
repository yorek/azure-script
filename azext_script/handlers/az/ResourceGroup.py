from azext_script.handlers.Handler import Handler
from azext_script.handlers.az.Generic import GenericHandler

class ResourceGroupHandler(GenericHandler):
    azure_object = "group"
 
    def execute(self):
        self.add_context_parameter("location", "location")

        cmd = super(ResourceGroupHandler, self).execute()

        self.save_to_context()

        return cmd
 
  