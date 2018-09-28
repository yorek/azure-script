import sys
from handlers.Handler import Handler
from handlers.az.Generic import *

class EventHubsHandler(GenericHandler):
    azure_object = "eventhubs"
    
    def execute(self, objects, name, params):
        fon = ' '.join(objects[0:-1])

        #print(fon)
        self.context_parameters = []

        if fon == "eventhubs eventhub consumer-group":
            self.context_parameters.append(ContextParameter("eventhub-name", "eventhubs eventhub"))
            self.context_parameters.append(ContextParameter("namespace-name", "eventhubs namespace"))
            self.context_parameters.append(ContextParameter("resource-group", "resource group"))

        if fon == "eventhubs eventhub":
            self.context_parameters.append(ContextParameter("namespace-name", "eventhubs namespace"))
            self.context_parameters.append(ContextParameter("resource-group", "resource group"))

        if fon == "eventhubs namespace authorization-rule keys list":
            self.context_parameters.append(ContextParameter("namespace-name", "eventhubs namespace"))
            self.context_parameters.append(ContextParameter("resource-group", "resource group"))

        if fon == "eventhubs namespace":
            self.context_parameters.append(ContextParameter("resource-group", "resource group"))
            self.context_parameters.append(ContextParameter("location", "location"))

        cmd = GenericHandler.execute(self, objects, name, params)

        self.set_context_value(objects, name)

        return cmd


 