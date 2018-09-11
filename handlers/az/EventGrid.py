from handlers.Handler import Handler

class EventGridHandler(Handler):
    azure_object = "eventgrid"
 
    def create(self, objects, name, params):
        cmd = "az"        
        if (objects[1] == "topic"):
            cmd += u" eventgrid topic create -g {0} -n {1}".format(self.context["resource-group"], name)
            cmd += u" -l {0}".format(self.context["location"])

        return cmd
 
   