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
        """
        Return full resource name
        """
        return ' '.join(self.resources)

    def save_to_context(self, key=None, value=None):
        """
        Push value into context.
        If 'key' is None, the full resource name will be used a key.
        If 'value' is None, the object name will be used a value.
        """
        if (key == None):
            key = self.get_full_resource_name()

        if (value == None):
            value = self.name

        #print("[{0}:{1}]".format(key, value))
        
        self.context[key] = value
