class Handler(object):
    context = None
    resources = None
    action = None
    params = None
    name = None

    def __init__(self, context, resources, action, name, params):
        self.context = context
        self.resources = resources
        self.action = action
        self.name = name
        self.params = params

    def get_full_resource_name(self):
        return ' '.join(self.resources)

    def save_to_context(self):
        key =  self.get_full_resource_name()
        #print("[{0}:{1}]".format(key, value))
        self.context[key] = self.name
