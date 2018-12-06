from .Generic import GenericHandler

class IoTHubHandler(GenericHandler):
    azure_object = "iot hub"
                
    def execute(self):
        wrapper = ""
        fqn = self.get_full_resource_name()
        
        self.add_context_parameter("resource-group", "group")
        
        if fqn == "iot hub" and self.action == "create":
            rg = self.get_param_value("resource-group")

            wrapper += "IOTHUB_EXISTS=`az iot hub list -g {0} -o json --query \"[].id\" | grep {1}` \n".format(rg, self.name)
            wrapper += "if [ -z $IOTHUB_EXISTS ]; then \n"
            wrapper += "    @cmd \n"
            wrapper += "fi"

        cmd = super(IoTHubHandler, self).execute()

        self.save_to_context()

        if self.target == "azsh":
            cmd.wrapper = wrapper        

        return cmd

class IotHubDeviceIdentity(GenericHandler):
    azure_object = "iot hub device-identity"
 
    def execute(self):
        wrapper = ""
        #self.add_command_depedency("azure-cli-iot-ext", "0.5.1")

        if self.action == "create":
            device_id = self.name
            self.params["device-id"] = device_id
            self.name = None
            self.add_context_parameter("hub-name", "iot hub")
            hub_name = self.get_param_value("hub-name")

            wrapper += "IOTDEVICE_EXISTS=`az iot hub device-identity list -n {0} -o json --query \"[].deviceId\" | grep {1}` \n".format(hub_name, device_id)
            wrapper += "if [ -z $IOTDEVICE_EXISTS ]; then \n"
            wrapper += "    @cmd \n"
            wrapper += "fi"

        cmd = super(IotHubDeviceIdentity, self).execute()

        self.save_to_context(value=device_id)

        if self.target == "azsh":
            cmd.wrapper = wrapper        

        return cmd

 
   