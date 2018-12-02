# Azure Script

A script language created to make deployment and management of Azure resources as simple and intelligent as possible. 
In order to have a near zero learning curve, and to leverage everything you already know about AZ CLI and to even help you to learn more about it, the language sytanx is very similar to AZ CLI commands. It also has some additional unique feature, but you can reuse all your existing AZ CLI experience to start using Azure Script right away.

It will significantly reduce the amount of custom code you need to write to execute AZ CLI commands and to create shell script to deploy your Azure resources.

Read more about Azure Script [here](#TODO).

[![Build Status](https://dev.azure.com/epicstuff/AZ%20CLI%20Script/_apis/build/status/Build)](https://dev.azure.com/epicstuff/AZ%20CLI%20Script/_build/latest?definitionId=27)

## This is an experiment

We created this project while coding with Azure customers. It is an experiment and not yet officially support and maintained by the AZ CLI team. Our customers found it useful and we think you might as well. Please give it a try, use it in your project, submit issues and help us continue to develop it.

## Goal

For this first realease the goal is to support all available AZ resources and:

- remove all redundancy: no need to specify the same options again and again. 
- keep command signature and options consistent across all commands: in some AZ commands the resource name is not specified using the --name option. AZ  Script will correct that.
- integrate with 3rd party CLI like Databricks CLI or Kubernetes CLI
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

- App Service
- Application Insight
- Cosmos DB
- Event Grid
- Event Hubs
- Extension
- Function App
- HDInsight
- Iot
- Resource Group
- Service Fabric
- SQL DB
- SQL Server
- Storage

More will come in near future, stay tuned.

## Install

Azure Script has been integrated into AZ CLI via Extensions. The extension has not been pushed in the official AZ CLI Extension repository yet, since is still under heavy development, but is nonetheless available by manually specifying the source. Just run this:
	
	az extension add --source https://aka.ms/azure_script-latest-py2.py3-none-any.whl

and you're done. You may want to take a look at the samples folder to get started with AZ CLI Script:

[Azure Script Samples](./samples)

## Usage

Run the `az script run` command, passing the script file you want to compile.

```
az script run --script <filename.azs> 
```

by default will generate the AZ CLI commands needed to do what defined in the script file.

As a starting sample you can use the `e2e-2.azs` script:

	az script run --script .\samples\e2e-2.azs

it will generate AZ CLI script ready to be executed in a [WSL](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux) bash.

### Full Bash Script generation

If you want to generate a full featured bash script you can use the `azsh` target:

	az script run --script .\samples\e2e-2.azs --target azsh

### File Output

The --output option will generate the code into the specified file instead of sending the result to the console

	az script run --script .\samples\e2e-2.azs --output-file .\samples\e2e-2.azs.sh

### Samples Notes

Please note that some samples requires additional file in order to properly run the resulting bash script. For example `package.zip` or `indexing.json` that are not provided since they are just used in the samples as placeholders to show what you can do with Azure Script.

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
- Run pre-validation checks (for example check that all files referenced in the script actually exists).
- Add an option to inject pre-validation checks into generated script, when appropriate (for example with AZ CLI)
- Add templating support (using [Jinjia](http://jinja.pocoo.org/ß))
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
