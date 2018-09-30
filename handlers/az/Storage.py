import sys
from handlers.Handler import Handler
from handlers.az.Generic import GenericHandler

class StorageShareHandler(GenericHandler):
    azure_object = "storage share"
 
    def execute(self):
        self.add_context_parameter("account-name", "storage account")

        cmd = super().execute()

        self.save_to_context()

        return cmd

class StorageHandler(GenericHandler):
    azure_object = "storage"
 
    def execute(self):
        self.add_context_parameter("resource-group", "group")
        self.add_context_parameter("location", "location")

        cmd = super().execute()

        self.save_to_context()

        return cmd
  
   
        
        