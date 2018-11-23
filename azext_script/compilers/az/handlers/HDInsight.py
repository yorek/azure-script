from .Generic import GenericHandler

class HDInsightHandler(GenericHandler):
    azure_object = "hdinsight"
    
    def execute(self):
        fqn = self.get_full_resource_name()
        
        self.add_context_parameter("resource-group", "group")

        if fqn == "hdinsight" and self.action == "create":            
            self.add_context_parameter("location", "location")
            if 'storage account' in self.context:
                storage_account = self.context["storage account"]
                storage_account += ".blob.core.windows.net"
                self.add_parameter("storage-account", storage_account)

        cmd = super(HDInsightHandler, self).execute()

        self.save_to_context()

        return cmd

