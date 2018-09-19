from handlers.Handler import Handler
import handlers.az

availabe_handlers = (vars()["Handler"].__subclasses__())

