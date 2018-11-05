import sys
from azext_script.handlers.Handler import Handler
from azext_script.handlers.az.Generic import GenericHandler

class CosmosDBHandler(GenericHandler):
    azure_object = "cosmosdb"

    def get_from_context(self, name):
        if name in self.context:
            return self.context[name]
        else:    
            print("***** MISSING '{}' in context".format(name))
            sys.exit(1)
        
    def execute(self):
        fqn = self.get_full_resource_name()
        cmd_wrapper = ""
        context_value = self.name

        if fqn == "cosmosdb":
            cmd_wrapper = "SERVER_EXISTS=`az cosmosdb check-name-exists -n {0} -o tsv`".format(self.name) + "\n"
            cmd_wrapper += "if [ $SERVER_EXISTS == ""false"" ]; then\n"
            cmd_wrapper += "  @cmd \n"
            cmd_wrapper += "fi"
            self.add_context_parameter("resource-group", "group")

        if fqn == "cosmosdb database":
            cmd_wrapper = "DB_EXISTS=`az cosmosdb database exists -g {0} -n {1} --db-name {2} -o tsv`".format(self.get_from_context("group"), self.get_from_context("cosmosdb"), self.name) + "\n"
            cmd_wrapper += "if [ $DB_EXISTS == ""false"" ]; then \n"
            cmd_wrapper += "  @cmd \n"
            cmd_wrapper += "fi"

            db_name = self.name
            self.params["db-name"] = db_name
            self.name = self.get_from_context("cosmosdb")
            self.add_context_parameter("resource-group", "group")

        if fqn == "cosmosdb collection":
            cmd_wrapper = "COLLECTION_EXISTS=`az cosmosdb collection exists -g {0} -n {1} --db-name {2} --collection-name {3} -o tsv`".format(self.get_from_context("group"), self.get_from_context("cosmosdb"), self.get_from_context("cosmosdb database"), self.name) + "\n"
            cmd_wrapper += "if [ $COLLECTION_EXISTS == ""false"" ]; then \n"
            cmd_wrapper += "  @cmd \n"
            cmd_wrapper += "fi"

            collection_name = self.name
            self.params["collection-name"] = collection_name
            self.name = self.get_from_context("cosmosdb")            
            self.add_context_parameter("db-name", "cosmosdb database")
            self.add_context_parameter("resource-group", "group")

        cmd = super(CosmosDBHandler, self).execute()

        self.save_to_context(fqn, context_value)

        if self.target == "azsh":
            r = cmd_wrapper.replace("@cmd", cmd[0]), cmd[1]
        else:
            r = cmd

        return r
