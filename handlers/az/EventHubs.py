import sys
from handlers.Handler import Handler
from handlers.az.Generic import GenericHandler

class EventHubsConsumerGroupHandler(GenericHandler):
    azure_object = "eventhubs eventhub consumer-group"
 
    def execute(self, objects, name, params):
        self._param_from_context(params, "eventhub-name", "eventhubs eventhub")
        self._param_from_context(params, "namespace-name", "eventhubs namespace")
        self._param_from_context(params, "resource-group", "resource group")

        cmd = GenericHandler.execute(self, objects, name, params)

        self.set_context_value(objects, name)

        return cmd

class EventHubsEventHubHandler(GenericHandler):
    azure_object = "eventhubs eventhub"
 
    def execute(self, objects, name, params):
        self._param_from_context(params, "namespace-name", "eventhubs namespace")
        self._param_from_context(params, "resource-group", "resource group")

        cmd = GenericHandler.execute(self, objects, name, params)

        self.set_context_value(objects, name)

        return cmd

class EventHubsNamespaceAuthorizationRuleKeysListHandler(GenericHandler):
    azure_object = "eventhubs namespace authorization-rule keys list"
 
    def execute(self, objects, name, params):
        self._param_from_context(params, "namespace-name", "eventhubs namespace")
        self._param_from_context(params, "resource-group", "resource group")

        cmd = GenericHandler.execute(self, objects, name, params)

        self.set_context_value(objects, name)

        return cmd

class EventHubsNamespaceHandler(GenericHandler):
    azure_object = "eventhubs namespace"
 
    def execute(self, objects, name, params):
        self._param_from_context(params, "resource-group", "resource group")
        self._param_from_context(params, "location", "location")

        cmd = GenericHandler.execute(self, objects, name, params)

        self.set_context_value(objects, name)

        return cmd
 