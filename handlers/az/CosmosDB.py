import sys
from handlers.Handler import Handler
from handlers.az.Generic import GenericHandler

class CosmosDBHandler(GenericHandler):
    azure_object = "cosmosdb"
 
    def execute(self, objects, name, params):
        if not "resource-group" in params:
            params["resource-group"] = self.context["resource group"]

        cmd = GenericHandler.execute(self, objects, name, params)

        self.set_context_value(objects, name)

        return cmd

class CosmosDBDatabaseHandler(CosmosDBHandler):
    azure_object = "cosmosdb database"
    
    def execute(self, objects, name, params):
        db_name = name
        params["db-name"] = db_name

        if "cosmosdb" in self.context:
            name = self.context["cosmosdb"]
        else:    
            print("***** MISSING 'cosmosdb' server name in context")
            sys.exit(1)

        cmd = CosmosDBHandler.execute(self, objects, name, params)

        self.set_context_value(objects, db_name)

        return cmd


class CosmosDBCollectionHandler(CosmosDBHandler):
    azure_object = "cosmosdb collection"

    def execute(self, objects, name, params):
        collection_name = name
        params["collection-name"] = collection_name

        if "cosmosdb" in self.context:
            name = self.context["cosmosdb"]
        else:    
            print("***** MISSING 'cosmosdb' server name in context")
            sys.exit(1)

        if "cosmosdb database" in self.context:
            db_name = self.context["cosmosdb database"]
            params["db-name"] = db_name
        else:    
            print("***** MISSING 'cosmosdb database' name in context")
            sys.exit(1)

        cmd = CosmosDBHandler.execute(self, objects, name, params)

        self.set_context_value(objects, collection_name)

        return cmd
