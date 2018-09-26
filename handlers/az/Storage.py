import sys
from handlers.Handler import Handler
from handlers.az.Generic import GenericHandler

class StorageShareHandler(GenericHandler):
    azure_object = "storage share"
 
    def execute(self, objects, name, params):
        if not "account-name" in params:
            if "storage account" in self.context:
                params["account-name"] = self.context["storage account"]                
            else:    
                print("***** MISSING 'account-name' option in command and no 'storage account' found")
                sys.exit(1)

        cmd = GenericHandler.execute(self, objects, name, params)

        self.set_context_value(objects, name)

        return cmd

class StorageHandler(GenericHandler):
    azure_object = "storage"
 
    def execute(self, objects, name, params):
        if not "resource-group" in params:
            params["resource-group"] = self.context["resource group"]

        if not "location" in params:
            params["location"] = self.context["location"]

        cmd = GenericHandler.execute(self, objects, name, params)

        self.set_context_value(objects, name)

        return cmd
  
   
        
        