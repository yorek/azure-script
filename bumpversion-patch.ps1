#
# This script will bump the patch version
#
# Note: 
# Version number is: mayor.minor.path
#
param (
    [Parameter(Mandatory=$true,HelpMessage="Specific if to TEST or do a REAL change")][string]$mode = "test"
)

if ($mode -eq "TEST")
{
    if (Test-Path -Path ".\env3\Scripts\activate") {
        .\env3\Scripts\activate
        bumpversion --dry-run --allow-dirty --verbose patch
        deactivate
    } else {
        Write-Error "'env3' Python 3.x virtual enviroment not found."
    }    
} 
elseif ($mode -eq "REAL")
{
    if (Test-Path -Path ".\env3\Scripts\activate") {
        .\env3\Scripts\activate
        bumpversion patch
        deactivate
    } else {
        Write-Error "'env3' Python 3.x virtual enviroment not found."
    }    
} 
else {
    Write-Error "-mode paramater is mandatory and must be set to 'TEST' or 'REAL'"
}


 

