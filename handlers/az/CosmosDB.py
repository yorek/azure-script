import sys
from handlers.Handler import Handler
from handlers.az.Generic import GenericHandler

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
        
        if fqn == "cosmosdb":
            self.add_context_parameter("resource-group", "group")

        if fqn == "cosmosdb database":
            db_name = self.name
            self.params["db-name"] = db_name
            self.name = self.get_from_context("cosmosdb")

        if fqn == "cosmosdb collection":
            collection_name = self.name
            self.params["collection-name"] = collection_name
            self.name = self.get_from_context("cosmosdb")            
            self.add_context_parameter("db-name", "cosmosdb database")

        cmd = super(CosmosDBHandler, self).execute()

        self.save_to_context()

        return cmd
