class Handler(object):
    context = None
    objects = None
    action = None
    params = None

    def __init__(self, context, objects):
        self.context = context
        self.objects = objects
        #print("objects: {0}".format(objects))
        #print("context: {0}".format(context))

    def set_context_value(self, objects, value):
        if objects[-1] == "create":
            key = ' '.join(objects[0:-1]) 
            #print("[{0}:{1}]".format(key, value))
            self.context[key] = value