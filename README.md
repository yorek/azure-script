# AZ CLI Script

A script language created from AZ CLI commands to make deployment and management of Azure resources as simple and intelligent as possible. It will significantly reduce the amount of custom code you need to write to execute Az CLI commands.

[![Build Status](https://dev.azure.com/epicstuff/AZ%20CLI%20Script/_apis/build/status/Build)](https://dev.azure.com/epicstuff/AZ%20CLI%20Script/_build/latest?definitionId=27)

## This is an experiment

We created this project while coding with Azure customers. It is an experiment and not yet officially support and maintained by the AZ CLI team. Our customers found it useful and we think you might as well. Please give it a try, use it in your project, submit issues and help us continue to develop it.

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

The (somehow) supported resources, right now, are

- appservice
- cosmosdb
- eventhubs
- extension
- functionapp
- iot
- resource group
- storage

More will come in near future, stay tuned.

## Install

If you're not interested into developing AZ CLI Script compiler, just use the usual `pip` tool:

	pip install azsc

Done. You may want to take a look at the samples folder to get started with AZ CLI Script:

[AZ CLI Script Samples](./samples)

## Usage

Just run the `azsc` compiler, passing the script file you want to compile.

```
azsc <filename.azs> [--debug]
```

will generate the AZ CLI commands needed to do what defined in the script file.
`--debug` will also print the parse tree for debugging purposes

As a starting sample you can use the `e2e-1.azs` script:

	azsc .\samples\e2e-1.azs

it will generate AZ CLI script ready to be executed in a [WSL](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux) bash.

## Compilation

The result of compiling is, at present time, a transpilation to AZ CLI commands. The entire process is completely extensibile, so in future plugins to generate ARM templates or even direct REST API calls could be created.

## Notes

Grammar definition is done using EBNF format and the parses is [Lark](https://github.com/lark-parser/lark)

## Roadmap

For now this is just an experiment. Let's see where it goes...

But if you're curious here's something I have in mind:

- Support 3rd party Azure Resources (like Azure Databricks) in order to provide a common, unified, infrastructure-as-code experience
- Support syntax highlighting Visual Studio Code (done: https://github.com/yorek/azure-script-vscode)
- Support for and code completion in Visual Studio Code
- Support running and debugging .azs script in Visual Studio Code
- Add templating support (using [Liquid](https://shopify.github.io/liquid/))
- Build a graph of dependencies and the run as many AZ CLI commands in parallel as possibile
- Using the dependency graph, validate the command even before running them
- Enforce application of best practies and well-know patterns
- Define a clever way to deal with erros like:
	- automatic retry 
	- break the scripts
	- take compensating actions
- Generate Powershell Script
- Generate ARM template
- Execute the commands instead of just generating a script
- Add an interactive mode

# Contributing

This project welcomes contributions and suggestions. Just fork the repository, make your changes and submit a Pull Request. 
