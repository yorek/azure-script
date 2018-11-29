class CommandResult: 
    pass

class AZCLICommand(CommandResult):
    source = None
    header = ""
    footer = ""
    wrapper = None
    assign_to = None

    def __init__(self, command, header="", footer="", wrapper = None, source=None):
        self.command = command
        self.header = header
        self.footer = footer
        self.source = source
        if (wrapper is not None and wrapper.strip() == ""):
            self.wrapper = None
        else:
            self.wrapper = wrapper

    def __str__(self):
        result = ""
        
        if self.assign_to is not None:
            result += "export {0}=$({1} -o tsv)".format(self.assign_to, self.command)
        else:
            # self.__result += " -o json >> azcli-execution.log"
            result += self.command + " -o json"
        
        if self.wrapper is not None:
            result = self.wrapper.format(self.command) 
        
        return result

class ExportCommand(CommandResult):
    name = ""
    value = ""
    
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return 'export {0}="{1}"'.format(self.name, self.value)           

class EchoCommand(CommandResult):
    message = ""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return '\necho "{0}"'.format(self.message)
        