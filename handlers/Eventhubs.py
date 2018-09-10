from Handler import Handler

class EventHubsHandler(Handler):
    azure_object = "eventhubs"
 
    def create(self, items):
        cmd = "az"
        cmd += " eventhubs"
        return cmd
 
    def select(self, items):
        pass

    def use(self, items):
        pass