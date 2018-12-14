class CommandResult: 
    target = "az"
    pass

class EmptyCommand(CommandResult):
    def __str__(self):
        return ""

class AZCLICommand(CommandResult):
    command = ""
    source = None
    header = ""
    footer = ""
    wrapper = None
    assign_to = None

    def __init__(self, command, header="", footer="", wrapper=None, source=None):
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
        command = ""

        if (self.target == "azsh"):            
            result += "echo \"{0}: {1} {2}\"\n".format(self.source.action, self.source.get_full_resource_name(), self.source.name or '')        

        if self.assign_to is not None:
            command += "export {0}=$({1} -o tsv)".format(self.assign_to, self.command)
        else:
            if (self.target == "azsh"):
                command += self.command + " -o json >> azcli-execution.log"                
            else:
                command += self.command + " -o table"            
        
        if self.wrapper is not None:
            command = self.wrapper.replace("@cmd", self.command) 
        
        result += command

        return "\n" + result

class ExportCommand(CommandResult):
    name = ""
    value = ""
    
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        if isinstance(self.value, AZCLICommand):
            self.value.assign_to = self.name
            self.value.target = self.target
            return str(self.value)
        else:
            return 'export {0}="{1}"'.format(self.name, self.value)           

        