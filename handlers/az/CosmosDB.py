from handlers.Handler import Handler

class CosmosDBHandler(Handler):
    azure_object = "cosmosdb"
 
    def create(self, objects, name, params):
        cmd = "az"
        cmd += u" {0} create -g {1} -n {2}".format(' '.join(objects), self.context["resource-group"], name)
        cmd += u" -l {0}".format(self.context["location"])

        for param in params:
            cmd += " --{0} {1}".format(param[0], param[1])

        return cmd
 