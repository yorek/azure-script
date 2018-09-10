from Handler import Handler

class EventGridHandler(Handler):
    azure_object = "eventgrid"
 
    def create(self, items):
        cmd = "az"
        cmd += " eventgrid"
        return cmd
 
    def select(self, items):
        pass

    def use(self, items):
        pass
