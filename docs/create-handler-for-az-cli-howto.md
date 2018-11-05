# Create an Handler to generate AZ CLI code

If an AZ CLI command is not yet 100% supported by Azure Script, you can easly create a new Handler to support it. It will take no more then 5 minutes and just 3 simple steps. Here's an example that shows how to create an Handler that will support and generate `az sql server` AZ CLI command.

## 1. Create the Handler in az folder

Create a new empty `.py` in `~/azsc/handlers/az` folder and the copy and paste the followin startup code:

    from azext_script.handlers.Handler import Handler
    from azext_script.handlers.az.Generic import GenericHandler

    class SqlServerHandler(GenericHandler):
        azure_object = "sql server"
        
        def execute(self):
            # get full resouce name
            fqn = self.get_full_resource_name()

            # create az cli command 
            cmd = super(SqlServerHandler, self).execute()

            # push object name into script context
            self.save_to_context()

            # return the generated command to the transformer
            return cmd

as you can see the code is really simple:

In the `azure_object` variable the handler tell the Transformer, the engine that take the parsed tree and turn it into something else, like AZ CLI command in this case, that it will handle all the lines of code related to the `sql server` Azure resource family.

The `execute` method will be called each time, in the Azure script code, a line starts with `sql server`.

## 2. Use context to add well-known values

Since one common use case is to create a SQL Server resource, let's focus on generating the correct `az sql server create` AZ CLI command.

The documentation (`az sql server create --help`) shows that it needs, aside the name, also the following mandatory parameters:

- `resource-group`
- `location`
- `admin-password`
- `admin-name`

values for `location` and `resource-group` should be taken from the context if possible. 

In a real-world script, the user will probabily set the location and the resource group that be must used throughout the script once and for all at the beginning of the script itself. The implied desired behaviour is that all following commands should be able to automatically take advantage of that information and use it when transpiling to AZ CLI commands. 

To achieve that, the handler needs to know which parameters can be inferred from context. The `add_context_parameter()` method takes care of this. Here's the updated code: 

    from azext_script.handlers.Handler import Handler
    from azext_script.handlers.az.Generic import GenericHandler

    class SqlServerHandler(GenericHandler):
        # The AZ object this handler will manage
        azure_object = "sql server"
        
        def execute(self):
            # use the value set by the "group" command
            # to fill the "resource-group" parameter
            self.add_context_parameter("resource-group", "group")

            # as above, take location set in the script and use it as parameter
            self.add_context_parameter("location", "location")

            # create az cli command 
            cmd = super(SqlServerHandler, self).execute()

            # push object name into script context
            self.save_to_context()

            # return the generated command to the transformer
            return cmd

## 2. Specify mandatory parameters

Some parameters cannot be derived from context and the user just need to specifiy them in the Azure Script code. To make sure the Azure Script engine know which parameters are mandatory `set_required_parameter()` has to be used.

The required `admin-user` and `admin-password` parameter are needed only by the `create` action. By checking the `action` field the code can make sure they are considered mandatory only when creating the resource.

Here's the updated code:

    from azext_script.handlers.Handler import Handler
    from azext_script.handlers.az.Generic import GenericHandler

    class SqlServerHandler(GenericHandler):
        # The AZ object this handler will manage
        azure_object = "sql server"
        
        def execute(self):
            # use the value set by the "group" command
            # to fill the "resource-group" parameter
            self.add_context_parameter("resource-group", "group")

            # as above, take location set in the script and use it as parameter
            self.add_context_parameter("location", "location")

            # make sure admin user and password are mandatory only
            # when generating the "az sql server create" command
            if (self.action == "create"):  
                # check that required parameters are actually provided
                self.set_required_parameter("admin-user")
                self.set_required_parameter("admin-password")

            # create az cli command 
            cmd = super(SqlServerHandler, self).execute()

            # push object name into script context
            self.save_to_context()

            # return the generated command to the transformer
            return cmd
            
## Extending the handler to manage other actions and resources

The `az sql server` command offer much more capabilities than just the creation of a Azure SQL Server resource. For example can manage server keys via `az sql server key` or can just query the existing Azure SQL Server resources using `az sql server list` command.

Exetending the newly created handler to support all the desired resources and commands can be done in two different ways.

### Option 1: Using the execute() method of created handler

The first way is using the fully qualified resource name, that can be obtained via the `get_full_resource_name()` method. It will return a string with all the resources specified in the Azure Script line. For example `sql server key` will be returned for the Azure Script

    sql server key create 'mykey';

command. This allows the handling of specific resources right in the body of handlers' `execute()` method. In additio to that you can also use the `action` field to know which action the use is requestion. The action is always the last token before the resource name. In the above sample, the action is `create` and the resource name is `mykey`.

### Option 2: Crearting more specialized Handlers

Another option, better if there are a lot of different sub-resources to manage (like the `key` ), is to create handler that take care that specific resources. The Transformer engine will most specilized handler available to handle each resource. For example an handler that tells the Transformer engine that it can manage the `sql server` resource will *not* be called if the code being compiled is `sql server key` and an handler that manages specifically the `sql server key` resource exists. In this way it is really easy to handle even very complex resources by followin a divide and conquer approach.

