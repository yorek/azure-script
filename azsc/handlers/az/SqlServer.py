from azsc.handlers.Handler import Handler
from azsc.handlers.az.Generic import GenericHandler

class SqlServerHandler(GenericHandler):
    # The AZ object this handler will manage
    azure_object = "sql server"
    
    def execute(self):
        fqn = self.get_full_resource_name()

        if (self.action == "create"):        
            # use the value set by the "group" command
            # to fill the "resource-group" parameter, required by "az sql server" command
            self.add_context_parameter("resource-group", "group")

            # as above, take location set in the script and 
            # use it as parameter
            self.add_context_parameter("location", "location")

            # check that required parameters are actually provided
            self.set_required_parameter("admin-user")
            self.set_required_parameter("admin-password")

        cmd = super(SqlServerHandler, self).execute()

        # push object name into script context
        self.save_to_context()

        return cmd

