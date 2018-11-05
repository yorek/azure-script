from .Generic import GenericHandler

class SqlServerHandler(GenericHandler):
    # The AZ object this handler will manage
    azure_object = "sql server"
    
    def execute(self):
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

class SqlServerFirewallRuleHandler(GenericHandler):
    azure_object = "sql server firewall-rule"
    
    def execute(self):
        if (self.action == "create"):        
            # add parameters from context
            self.add_context_parameter("resource-group", "group")
            self.add_context_parameter("server", "sql server")

            # check that required parameters are actually provided
            self.set_required_parameter("start-ip-address")
            self.set_required_parameter("end-ip-address")

        cmd = super(SqlServerFirewallRuleHandler, self).execute()

        # push object name into script context
        self.save_to_context()

        return cmd
