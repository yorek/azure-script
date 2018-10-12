az group create --name "dmiottest" --location "eastus"
az extension add --name "azure-cli-iot-ext"
az iot hub create --name "dmiothubtest" --sku "F1" --resource-group "dmiottest"
az iot hub device-identity create --name "mydevice" --hub-name "dmiothubtest"
