#!/bin/bash

az group create --name "dmk1" --location "eastus"
az storage account create --name "dmk1storage" --sku "Standard_LRS" --resource-group "dmk1" --location "eastus"
az eventhubs namespace create --name "dmk1ingest" --sku "Standard" --capacity 20 --resource-group "dmk1" --location "eastus"
az eventhubs eventhub create --name "dmk1ingest-32" --message-retention 1 --partition-count 32 --namespace-name "dmk1ingest" --resource-group "dmk1"
az eventhubs eventhub consumer-group create --name "cosmos" --eventhub-name "dmk1ingest-32" --namespace-name "dmk1ingest" --resource-group "dmk1"
az cosmosdb create --name "dmk1cosmosdb" --resource-group "dmk1"
az cosmosdb database create --name "dmk1cosmosdb" --db-name "streaming"
az cosmosdb collection create --name "dmk1cosmosdb" --partition-key-path "/eventData/eventId" --throughput 20000 --indexing-policy "{'indexingMode': 'none'}" --collection-name "rawdata" --db-name "dmk1cosmosdb"
az appservice plan create --name "dmk1plan" --number-of-workers 4 --sku "P1" --resource-group "dmk1"
az functionapp create --name "dmk1func" --resource-group "dmk1" --plan "dmk1plan" --storage-account "dmk1storage"
az functionapp deployment source config-zip --name "dmk1func" --src "package.zip"
export EVENTHUB_CS=$(az eventhubs namespace authorization-rule keys list --name "RootManageSharedAccessKey" --query "primaryConnectionString")
az functionapp config appsettings set --name "dmk1func" --settings "EventHubsConnectionString=$EVENTHUB_CS"
