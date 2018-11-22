from .Generic import GenericHandler

class ServiceFabricClusterHandler(GenericHandler):
    azure_object = "sf cluster"
 
    def execute(self):
        self.add_context_parameter("resource-group", "group")

        if (self.action == "create"):
            self.add_context_parameter("location", "location")
            self.set_required_parameter(["certificate-subject-name", "certificate-file", "secret-identifier"])

        cmd = super(ServiceFabricClusterHandler, self).execute()

        self.save_to_context()

        return cmd
        