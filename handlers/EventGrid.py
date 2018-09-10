from Handler import Handler

class EventGridHandler(Handler):
    azure_object = "eventgrid"
 
    def create(self, items):
        cmd = "az"        
        if (items[1] == "topic"):
            cmd += u" eventgrid topic create -g {0} -n {1}".format(self.context["resource-group"], items[2])
            cmd += u" -l {0}".format(self.context["location"])

        return cmd
 
    def select(self, items):
        pass

    def use(self, items):
        pass
