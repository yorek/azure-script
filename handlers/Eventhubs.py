from Handler import Handler

class EventHubsHandler(Handler):
    azure_object = "eventhubs"
 
    def create(self, items):
        cmd = "az"
        cmd += u" eventhubs {0} create -g {1} -n {2}".format(items[1], self.context["resource-group"], items[2])
        cmd += u" -l {0}".format(self.context["location"])

        return cmd
 
    def select(self, items):
        pass

    def use(self, items):
        pass