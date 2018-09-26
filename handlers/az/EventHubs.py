import sys
from handlers.Handler import Handler
from handlers.az.Generic import GenericHandler

class EventHubsConsumerGroupHandler(GenericHandler):
    azure_object = "eventhubs eventhub consumer-group"
 
    def execute(self, objects, name, params):
        if not "eventhub-name" in params:
            if "eventhubs eventhub" in self.context:
                params["eventhub-name"] = self.context["eventhubs eventhub"]                
            else:    
                print("***** MISSING 'eventhub-name' option in command and no 'eventhubs eventhub' found")
                sys.exit(1)

        if not "namespace-name" in params:
            if "eventhubs namespace" in self.context:
                params["namespace-name"] = self.context["eventhubs namespace"]                
            else:    
                print("***** MISSING 'namespace-name' option in command and no 'eventhubs namespace' found")
                sys.exit(1)

        if not "resource-group" in params:
            params["resource-group"] = self.context["resource group"]

        cmd = GenericHandler.execute(self, objects, name, params)

        self.set_context_value(objects, name)

        return cmd

class EventHubsEventHubHandler(GenericHandler):
    azure_object = "eventhubs eventhub"
 
    def execute(self, objects, name, params):
        if not "namespace-name" in params:
            if "eventhubs namespace" in self.context:
                params["namespace-name"] = self.context["eventhubs namespace"]                
            else:    
                print("***** MISSING 'namespace-name' option in command and no 'eventhubs-namespace' found")
                sys.exit(1)

        if not "resource-group" in params:
            params["resource-group"] = self.context["resource group"]

        cmd = GenericHandler.execute(self, objects, name, params)

        self.set_context_value(objects, name)

        return cmd

class EventHubsNamespaceHandler(GenericHandler):
    azure_object = "eventhubs namespace"
 
    def execute(self, objects, name, params):
        if not "resource-group" in params:
            params["resource-group"] = self.context["resource group"]

        if not "location" in params:
            params["location"] = self.context["location"]

        cmd = GenericHandler.execute(self, objects, name, params)

        self.set_context_value(objects, name)

        return cmd
 