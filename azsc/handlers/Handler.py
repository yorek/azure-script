class Handler(object):
    """
    The basic Handler class, that provides access to the active context, shared between all script commands
    and details about the command being parsed
    """
    
    context = {}
    """
    A dictionary that contains all the values pushed into the active context,
    shared between all commands in the script
    """
    
    resources = None
    """
    The resource objects, as array of strings, used by the command being parsed
    """

    action = None
    """
    The action specified by the command being parsed
    """

    params = {}
    """
    The parameters, if any, specified in the command being parsed
    """

    name = None
    """ 
    The object name target of command being parsed
    """

    target = None
    """
    transpilation target
    """

    def __init__(self, context, resources, action, name, params, target):
        self.context = context
        self.resources = resources
        self.action = action
        self.name = name
        self.params = params
        self.target = target

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
