from azext_script.handlers.Handler import Handler
from azext_script.handlers.az.Generic import GenericHandler

class IoTHubHandler(GenericHandler):
    azure_object = "iot hub"
    
    def execute(self):
        fqn = self.get_full_resource_name()
        
        if fqn == "iot hub":
            self.add_context_parameter("resource-group", "group")

        cmd = super(IoTHubHandler, self).execute()

        self.save_to_context()

        return cmd

class IotHubDeviceIdentity(GenericHandler):
    azure_object = "iot hub device-identity"
 
    def execute(self):
        device_id = self.name
        self.params["device-id"] = device_id
        self.name = None
        self.add_context_parameter("hub-name", "iot hub")

        cmd = super(IotHubDeviceIdentity, self).execute()

        self.save_to_context(value=device_id)

        return cmd

 
   