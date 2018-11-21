from .Generic import GenericHandler

class EventGridHandler(GenericHandler):
    azure_object = "eventgrid"
 
    
class EventGridTopicHandle(GenericHandler):
    azure_object = "eventgrid topic"

    def execute(self):

        if (self.action == "create"):
            self.add_context_parameter("resource-group", "group")
            self.add_context_parameter("location", "location")

        cmd = super(EventGridTopicHandle, self).execute()

        self.save_to_context()

        return cmd
        

class EventGridSubscriptionHandle(GenericHandler):
    azure_object = "eventgrid event-subscription"

    def execute(self):
        
        if (self.action == "create"):
            self.add_context_parameter("resource-group", "group")
            self.add_context_parameter("topic-name", "eventgrid topic")
            self.set_required_parameter("endpoint")

        cmd = super(EventGridSubscriptionHandle, self).execute()

        self.save_to_context()

        return cmd
        
