import re
import os.path
from io import open # pylint: disable=W0622
from setuptools import setup, find_packages

#
# Define objects and functions
#
package_folder_path = 'azext_script'

# Version extraction inspired from 'requests'
def load_version():
    with open(os.path.join(package_folder_path, '_constants.py'), 'r') as fd:
        return re.search(r'^VERSION\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

def load_readme():
    """
    Load README.md file if not running from inside a test tool like tox.
    """
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    readme_path = os.path.join(location, "README.md")

    if os.path.exists(readme_path):
        with open(readme_path, 'r') as fh:
            long_description = fh.read()
    else:
            long_description = ""

    return long_description


VERSION = load_version()

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Operating System :: OS Independent",
    "Topic :: Internet",
    "Topic :: Software Development :: Code Generators",
    "Topic :: Software Development :: Interpreters",
    "Topic :: Utilities",
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: MIT License',
]

DEPENDENCIES = [
    'lark-parser==0.6.4'
]

#
# Run setup
#

setup(
    name="azure-script",
    version=VERSION,
    author="Davide Mauri",
    author_email="info@davidemauri.it",
    license='MIT',
    description="A script language to make deployment and management of Azure resources as simple and intelligent as possibile.",
    long_description=load_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yorek/azure-script",
    packages=find_packages(),
    package_data={'azext_script': ['grammar/*.lark', 'compilers/az/handlers/simple-handlers/*.json']},
    classifiers=CLASSIFIERS,
    install_requires=DEPENDENCIES        
)