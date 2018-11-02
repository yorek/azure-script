# Contribute

This project welcomes contributions and suggestions. Just fork the repository, make your changes and submit a Pull Request. 

## Contributor Dev Machine Setup

If you want to help in developing Azure Script compiler, is strongly recommended that you use virtualenv to setup a isolated environment:

	virtualenv env3 --python=<path_to_python_3>

in my case, since I have installed Python 3 as part of Visual Studio 2017, the full command is the following:

	virtualenv env3 --python="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\python.exe"

and then activate it (for Linux see [here](https://virtualenv.pypa.io/en/stable/userguide/#usage))

	.\env3\Scripts\activate

you can then install required packages:

	pip install -e .

and you're done, you can start using it.

It is recommended to create two virtual environments, one for Python 2.7 and one for Python 3.x, named `env2` and `env3` respectively. 

