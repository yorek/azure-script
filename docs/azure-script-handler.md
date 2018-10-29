# Create an Handler

## Azure Script commands

An Azure Script command has to followin grammar:

    resource_name_part [resource_name_part...resource_name_part] action 'name';

for example

    storage account create 'mystorage';

the resource name parts identify the Azure resource you want to manage: 

- `resource` = storage account
- `action` = create
- `name` = mystorage

Almost any command supports parameters. For example the storage account allows to SKU level to be specified:

    storage account create 'mystorage' (
        sku: 'Standard_LRS'		
    );

In the above sample everything into the paranthe

## Command handlers

An handler is a class the derives from `Handler` class. Such class provides access to all the tokens used in the command being parsed.
- `resources`
- `action`
- `name`
- `param`

it also provide access to the `context` object that is shared between all script commands.

