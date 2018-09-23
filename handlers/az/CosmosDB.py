import sys
from handlers.Handler import Handler

class CosmosDBHandler(Handler):
    azure_object = "cosmosdb"
 
    def create(self, objects, name, params):
        cmd = "az"
        cmd += u" {0} create -g {1} -n {2}".format(' '.join(objects), self.context["resource group"], name)
        
        for param in params:
            cmd += " --{0} {1}".format(param[0], param[1])

        self.set_context_value(objects, name)

        return cmd

class CosmosDBDatabaseHandler(CosmosDBHandler):
    azure_object = "cosmosdb database"
    
    def create(self, objects, name, params):
        db_name = name
        params.append(["db-name", db_name])

        if "cosmosdb" in self.context:
            name = self.context["cosmosdb"]
        else:    
            print("***** MISSING 'cosmosdb' server name in context")
            sys.exit(1)

        cmd = CosmosDBHandler.create(self, objects, name, params)

        self.set_context_value(objects, db_name)

        return cmd


class CosmosDBCollectionHandler(CosmosDBHandler):
    azure_object = "cosmosdb collection"

    def create(self, objects, name, params):
        collection_name = name
        params.append(["collection-name", collection_name])

        if "cosmosdb" in self.context:
            name = self.context["cosmosdb"]
        else:    
            print("***** MISSING 'cosmosdb' server name in context")
            sys.exit(1)

        if "cosmosdb database" in self.context:
            db_name = self.context["cosmosdb database"]
            params.append(["db-name", db_name])
        else:    
            print("***** MISSING 'cosmosdb database' name in context")
            sys.exit(1)

        cmd = CosmosDBHandler.create(self, objects, name, params)

        self.set_context_value(objects, collection_name)

        return cmd
