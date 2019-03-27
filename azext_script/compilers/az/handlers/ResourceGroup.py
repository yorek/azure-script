from .Generic import GenericHandler

class ResourceGroupHandler(GenericHandler):
    azure_object = "group"
    
    def execute(self):       
        cmd = super(ResourceGroupHandler, self).execute()

        self.save_to_context()

        return cmd

