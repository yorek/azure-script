#
# This script will bump the patch version
#
# Note: 
# Version number is: mayor.minor.path
#

if (Test-Path -Path ".\env3\Scripts\activate") {
    .\env3\Scripts\activate
    bumpversion patch
    deactivate
} else {
    Write-Error "'env3' Python 3.x virtual enviroment not found."
}
