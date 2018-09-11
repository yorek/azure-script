from handlers.Handler import Handler

class EventHubsHandler(Handler):
    azure_object = "eventhubs"
 
    def create(self, objects, name, params):
        cmd = "az"
        cmd += u" {0} create -g {1} -n {2}".format(' '.join(objects), self.context["resource-group"], name)
        cmd += u" -l {0}".format(self.context["location"])

        return cmd
 