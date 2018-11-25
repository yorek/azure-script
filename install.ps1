$env:AZURE_EXTENSION_DIR="$env:HOME\.azure\devcliextensions\"
Write-Host "Installing to $env:AZURE_EXTENSION_DIR..."
pip install --upgrade --target $env:AZURE_EXTENSION_DIR\azure-script .
Write-Host "Done"
