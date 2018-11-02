#
# This script will build python packages
# for Python 2 and Python 3
#

if (Test-Path -Path ".\env2\Scripts\activate") {
    .\env2\Scripts\activate
    python setup.py sdist bdist_wheel
    deactivate    
} else {
    Write-Error "'env2' Python 2.7 virtual enviroment not found."
}

if (Test-Path -Path ".\env3\Scripts\activate") {
    .\env3\Scripts\activate
    python setup.py sdist bdist_wheel
    deactivate    
} else {
    Write-Error "'env3' Python 3.x virtual enviroment not found."
}


