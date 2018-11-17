from .Generic import GenericHandler

class ResourceGroupHandler(GenericHandler):
    azure_object = "group"
 
    def execute(self):
        self.add_context_parameter("location", "location")

        cmd = super(ResourceGroupHandler, self).execute()

        self.save_to_context()

        return ""
 
  