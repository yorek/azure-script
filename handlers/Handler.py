class Handler(object):
    context = None

    def __init__(self, context):
        self.context = context

    def set_context_value(self, objects, value):
        key = '-'.join(objects) 
        print("[{0}:{1}]".format(key, value))
        self.context[key] = value