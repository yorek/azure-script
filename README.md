# AZ Script

A script language created from AZ CLI commands to make deployment and management of Azure resources as simple and intelligent as possibile. It helps to reduce by 40% the code you need to write!

## Goal
For this first realease the goal is to support all available AZ CLI commands and:

- remove all redundancy: no need to specify the same options again and again. 
- keep command signature and options consistent across all commands: in some AZ commands the resource name is not specified using the --name option. AZ  Script will correct that.
- provide context-aware environment so every command knows what happened before and can act accordingly

For example, if you want all your resources deployed into the 'eastus' region you can just write

```
location use 'eastus';
```

and all subsequent command will use that location, if not explicity overridden in the command itself. **Same logic can be applied to any resource that depend on other resource.** Storage accounts for example, or VPNs.

## Language
The language has been created so that you can reuse everything you already know from AZ CLI. For example to create a storage account with AZ CLI you would type something like

```
az group create -n 'dmk1' -l 'eastus'
az storage account create -g 'dmk1' -n 'dmk1storage' -l 'eastus' --sku 'Standard_LRS'
az eventhubs namespace create -g 'dmk1' -n 'dmk1ingest' -l 'eastus' --sku 'Standard' --capacity 20
az eventhubs eventhub create -g 'dmk1' -n 'dmk1ingest-32' --message-rention 1 --partition-count 32 --namespace-name 'dmk1ingest'
az eventhubs eventhub consumer-group create -g 'dmk1' -n 'cosmos' --eventhub-name 'dmk1ingest-32' --namespace-name 'dmk1ingest'
```

with AZ Script you would write

```
location use 'eastus';

group create 'dmk1';

storage account create 'dmk1storage' (
	sku: 'Standard_LRS'		
);

eventhubs namespace create 'dmk1ingest' (
	sku: "Standard",
	capacity: 20
);

eventhubs eventhub create 'dmk1ingest-32' (
	message-retention: 1,
	partition-count: 32
);

eventhubs eventhub consumer-group create 'cosmos';
```
 
isn't that so much better?

## Extensibility
AZ Script is written in Python and can easily be extended to support any kind of Azure resource just by writing a simple plugin, which is nothing more than a class derived from the base class ```Handler```. Really easy!.

The supported resources, right now, are

- appservice
- cosmosdb
- functionapp
- eventhubs
- resource group
- storage

More will come in near future, stay tuned.

## Install
TDB

## Usage
Just run the `azsc` compiler, passing the script file you want to compile.

```
azsc <filename.azs> [--debug]
```

will generate the AZ CLI commands needed to do what defined in the script file.
`--debug` will also print the parse tree for debugging purposes

## Compilation
The result of compiling is, at present time, a transpilation to AZ CLI commands. The entire process is completely extensibile, so in future plugins to generate ARM templates or even direct REST API calls could be created.

## Notes
Grammar definition is done using EBNF format and the parses is [Lark](https://github.com/lark-parser/lark)

## Roadmap
For now this is just an experiment. Let's see where it goes...
