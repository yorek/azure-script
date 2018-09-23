from handlers.Handler import Handler
import handlers.az

def all_subclasses(cls):
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_subclasses(c)])

# find all hanlders (classes derived from Handler)
available_handlers = all_subclasses(Handler)

#print(available_handlers)


