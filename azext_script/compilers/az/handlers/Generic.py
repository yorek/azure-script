import sys
import collections
import json
import glob
import os
from azext_script.compilers.Handler import Handler
from azext_script.compilers.az.transformer.TranspilationResult import AZCLICommand
from knack.log import get_logger

logger = get_logger(__name__)

class Parameter:
    value = None
    omit_quotes = False

    def __init__(self, value, omit_quotes = False):
        self.value = value    
        self.omit_quotes = omit_quotes

    def __str__(self):
        return self.value

class ContextParameter:
    name = None
    context = None

    def __init__(self, name, context):
        self.name = name
        self.context = context

    def __eq__(self, other):
        if isinstance(other, ContextParameter):
            return self.name == other.name
                
        return self.name == str(other)
    
    def __str__(self):
        return "{0} => {1}".format(self.name, self.context)
        
class GenericHandler(Handler):
    azure_object = "*"    

    context_parameters = []
    required_parameters = []
    simple_handlers = {}

    def __init__(self, context, resources, action, name, params, target):
        super(GenericHandler, self).__init__(context, resources, action, name, params, target)
        self.context_parameters = []
        self.required_parameters = []

        # Load simple handlers json
        self.simple_handlers["handlers"] = []
        simple_handlers_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))   
        logger.debug("Looking from simple handlers definition in '{0}'".format(simple_handlers_location))          
        for f in glob.glob(os.path.join(simple_handlers_location, './simple-handlers/*.json')):
            if os.path.basename(f) != 'SimpleHandlers.schema.json':
                logger.debug("Found simple handler definition '{0}'. Adding to dictionary.".format(os.path.basename(f)))
                with open(f, 'r') as sc:                    
                    lsd = json.load(sc)
                    for h in lsd["handlers"]:
                        self.simple_handlers["handlers"].append(h)
                    

    def execute(self):
        fqn = self.get_full_resource_name()

        cmd = u"az"
        cmd += u" {0}".format(fqn)
        cmd += u" {0}".format(self.action)
        
        if (self.name != None):
            cmd += u' --name "{0}"'.format(self.name)
 
        # Load parameter mapping and info from json file, if available
        self._load_from_json()
        
        #print("-> {0} {1} {2}".format(self.resources, self.action, self.name))
        #print("-> CONTEXT: {0}".format(self.context))
        #print("-> PARAM_CONTEXT: {0}".format(self.context_parameters))

        # push parameters from values available in the context
        for cp in self.context_parameters:
            self._set_param_from_context(cp.name, cp.context)            
        
        # check that all required parameters are set
        for rp in self.required_parameters:
            #print(rp)
            #print(type(rp))
            if type(rp) == type('str'):
                if not rp in self.params:
                    print("ERROR:")
                    print("-> RESOURCE: " + self.azure_object)                
                    print("-> NAME: " + (self.name or "(unknown)"))
                    print("-> PARAM: {0}".format(rp))
                    sys.exit("Missing '{0}' required parameter.".format(rp))
            if type(rp) == type([]):
                found = False
                for p in rp:
                    #print("CHECKING: {0}".format(p))
                    if p in self.params:
                        found = True
                        break
                if not found:
                    print("ERROR:")
                    print("-> RESOURCE: " + self.azure_object)                
                    print("-> NAME: " + (self.name or "(unknown)"))
                    print("-> PARAM: one of {0}".format(rp))
                    sys.exit("Missing one of '{0}' required parameter.".format(rp))

        # add params to generated command line 
        if (len(self.params)>0):
            ordered_params = collections.OrderedDict(sorted(self.params.items()))
            for param in ordered_params:
                value = self.params[param]
                quote = '"'                

                if isinstance(value, Parameter):
                    if value.omit_quotes == True:
                        quote = ""
                else:
                    if '"' in value:
                        quote = "'"

                    if "'" in value:
                        quote = '"'

                if isinstance(value, Parameter):
                    if value.omit_quotes == True:
                        quote = ""

                value = quote + str(value) + quote

                cmd += u" --{0} {1}".format(param, value)

        return AZCLICommand(cmd, source=self)
 
    def derive_name_from_context(self, context_name):
         if context_name in self.context and self.name is None:
                self.name = self.context[context_name] 

    def add_context_parameter(self, parameter_name, context_name):
        """Specify how to map a context value to a parameter value
        
        parameter_name: parameter name. eg: resource-group

        context_name: context that holds the value to be passed to the paramter. eg: group        
        """
        self.context_parameters.append(ContextParameter(parameter_name, context_name))
        
    def add_parameter(self, parameter_name, parameter_value):
        self.params[parameter_name] = parameter_value

    def get_param_value(self, name):
        """Return the value of the specified parameter. If parameter is not present, will look in the context, using the provided mapping

        name: parameter name
        """
        if name in self.params:
            return self.params[name]

        context_name = [ cp.context for cp in self.context_parameters if cp.name == name ][0]

        if context_name is not None:
            return self.context[context_name]
        else:    
            message = "Missing '{0}' in parameters or context".format(name)
            raise(Exception(message))


    def set_required_parameter(self, parameters):
        """Mark parameters as mandatory

        parameters: use a string to specify a mandatory parameter; use a list to specify a list of parameters where at least one is mandotory      
        """

        if not parameters in self.required_parameters:
            #print("REQUIRED: {0}".format(parameters))
            self.required_parameters.append(parameters) 

    def _set_param_from_context(self, param_name, context_name):
        if not param_name in self.params:
            if context_name in self.context:
                self.params[param_name] = self.context[context_name]
            else:                    
                print("ERROR:")
                print("-> RESOURCE: " + self.azure_object)                
                print("-> NAME: " + (self.name or "(unknown)"))
                print("-> CONTEXT: {0}".format(self.context))
                print("-> PARAM_CONTEXT: {0}".format(self.context_parameters))
                sys.exit("Missing '{0}' parameter and not suitable context value '{1}' found.".format(param_name, context_name))

    def _load_from_json(self):
        fqn = self.get_full_resource_name()

        for h in self.simple_handlers["handlers"]:
            # Just for now. Same logic used for leading the most specialized
            # handler must be used also here. 
            # TODO: apply only the most specific handler configuration 
            # JSON should be loaded as a "static/class" method
            if fqn.startswith(h["azure_object"]):
                logger.debug("Found JSON Simple Handler defintion for resource '{0}'".format(fqn))  
                if "context_parameters" in h:
                    for cp in h["context_parameters"]:
                        self.add_context_parameter(cp["parameter"], cp["context"])  
                if "actions" in h:
                    for a in h["actions"]: 
                        if a["action"] == self.action:
                            logger.debug("Found action {0}".format(self.action))
                            if "context_parameters" in a:
                                for cp in a["context_parameters"]:
                                    self.add_context_parameter(cp["parameter"], cp["context"])  
                            if "required_parameters" in a:
                                for rp in a["required_parameters"]:
                                    self.set_required_parameter(rp)