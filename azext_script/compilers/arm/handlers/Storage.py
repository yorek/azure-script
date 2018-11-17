from .Generic import GenericHandler
import json

class StorageHandler(GenericHandler):
    azure_object = "storage"

    arm = {
        "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "resources": [
            {
                "type": "Microsoft.Storage/storageAccounts", 
                "apiVersion": "2018-07-01", 
                "sku": {  
                },
            }
        ]
    }

    def execute(self):
        storage = self.arm["resources"][0]

        storage["name"] = self.name
        storage["location"] = self.context["location"]

        if 'sku' in self.params:
            storage["sku"]["name"] = self.params["sku"]

        storage["kind"] = self.params["kind"]

        result = json.dumps(self.arm, indent=4)

        #cmd = super(StorageHandler, self).execute()

        #self.save_to_context()

        return result
  
   
        
        