#!/bin/sh

rm -rf ~/.azure/devcliextension/azure-script

pip install --upgrade --target ~/.azure/devcliextension/azure-script .

export AZURE_EXTENSION_DIR=~/.azure/devcliextension

az extension list --output table