import sys
from handlers.Handler import Handler
from handlers.az.Generic import GenericHandler

class EventHubsHandler(GenericHandler):
    azure_object = "eventhubs"
    
    def execute(self):
        fqn = self.get_full_resource_name()
        
        if fqn == "eventhubs eventhub consumer-group":
            self.add_context_parameter("eventhub-name", "eventhubs eventhub")
            self.add_context_parameter("namespace-name", "eventhubs namespace")
            self.add_context_parameter("resource-group", "group")

        if fqn == "eventhubs eventhub":
            self.add_context_parameter("namespace-name", "eventhubs namespace")
            self.add_context_parameter("resource-group", "group")

        if fqn == "eventhubs namespace authorization-rule keys list":
            self.add_context_parameter("namespace-name", "eventhubs namespace")
            self.add_context_parameter("resource-group", "group")

        if fqn == "eventhubs namespace":
            self.add_context_parameter("resource-group", "group")
            self.add_context_parameter("location", "location")

        cmd = super().execute()

        self.save_to_context()

        return cmd


 