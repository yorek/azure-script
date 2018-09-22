from handlers.Handler import Handler

class EventHubHandler(Handler):
    azure_object = "eventhubs eventhub"
 
    def create(self, objects, name, params):
        cmd = "az"
        cmd += u" {0} create -g {1} -n {2}".format(' '.join(objects), self.context["resource-group"], name)
        cmd += u" -l {0}".format(self.context["location"])

        for param in params:
            cmd += " --{0} {1}".format(param[0], param[1])

        if not "namespace-name" in params:
            if "eventhubs-namespace" in self.context:
                cmd += u" --namespace-name {0}".format(self.context["eventhubs-namespace"])
            else:    
                print("***** MISSING 'namespace-name' option in command and no 'eventhubs-namespace' found")
                sys.exit(1)

        self.set_context_value(objects, name)

        return cmd

class EventHubsHandler(Handler):
    azure_object = "eventhubs namespace"
 
    def create(self, objects, name, params):
        cmd = "az"
        cmd += u" {0} create -g {1} -n {2}".format(' '.join(objects), self.context["resource-group"], name)
        cmd += u" -l {0}".format(self.context["location"])

        for param in params:
            cmd += " --{0} {1}".format(param[0], param[1])

        self.set_context_value(objects, name)

        return cmd
 