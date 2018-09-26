class Handler(object):
    context = None

    def __init__(self, context):
        self.context = context

    def set_context_value(self, objects, value):
        if objects[-1] == "create":
            key = ' '.join(objects[0:-1]) 
            #print("[{0}:{1}]".format(key, value))
            self.context[key] = value