# AZ Script

A script language created from AZ CLI commands to make deployment and management of Azure Resource easier and straightforward. 

## Goal
The goal is to have a language that is just like AZ CLI command but with less overhead and more clever, make deployment automation a breeze.
For example, if you want all your resources deployed into the 'eastus' region you can just write

```
location use 'eastus';
```

and all subsequent command will use that location, if not explicity overridden in the command itself. Same logic can be applied to any resource that depend on other resource. Storage accounts for example, or VPNs.

## Language
The language has been created so that you can reuse everything you already know from AZ CLI. for example to create a storage account with AZ CLI you would type something like

```
az storage account create --resource-group 'myrg' --name 'mystorage' --sku='Standard_LRS' --location 'eastus'
```

with AZ Script you would write

```
location use 'eastus'
resource group use 'myrg'
storage account create 'storage' ( 
  sku = 'Standard_LRS'
)
```
 
isn't that so much better?

## Extensibility
AZ Script is written in python and can easily be extended to support any kind of Azure Resource just by writing a simple plugin, which is nothing more than a class derived from the base class ```Handler```. Really easy!.

## Transpilation
The result of transpiling is also extensibile. For now the result is a script of AZ CLI commands, but it can be replaced to generate ARM templates or even direct REST API calls if you really want.

## Roadmap
For now this is just an experiment. Let's see where it goes...
