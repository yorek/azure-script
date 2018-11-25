class CommandResult: 
    command = ""

class AZCLICommand(CommandResult):
    source = None
    header = ""
    footer = ""
    assign_to = None

    def __init__(self, command, header="", footer="", source=None):
        self.command = command
        self.header = header
        self.footer = footer
        self.source = source

class EchoCommand(CommandResult):
    def __init__(self, command):
        self.command = command       