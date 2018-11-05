import logging

from .Generic import GenericHandler

class SqlDbHandler(GenericHandler):
    azure_object = "sql db"
    
    def execute(self):
        fqn = self.get_full_resource_name()
        logging.debug("ACTION: " + self.action + " RESOURCE: " + fqn + " NAME: " + self.name)

        if (self.action == "create"):        
            self.add_context_parameter("resource-group", "group")
            self.add_context_parameter("server", "sql server")

        cmd = super(SqlDbHandler, self).execute()

        self.save_to_context()

        return cmd

