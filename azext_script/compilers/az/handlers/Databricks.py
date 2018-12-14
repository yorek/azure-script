from .Generic import GenericHandler

class DatabricksHandler(GenericHandler):
    azure_object = "databricks"
    
    def execute(self):       
        cmd = super(DatabricksHandler, self).execute()

        self.save_to_context()

        return cmd

