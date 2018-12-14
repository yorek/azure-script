from .Generic import GenericHandler

class ActiveDirectoryHandler(GenericHandler):
    azure_object = "ad"
    
    def execute(self):       
        cmd = super(ActiveDirectoryHandler, self).execute()

        self.save_to_context()

        return cmd

