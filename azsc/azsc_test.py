from __future__ import absolute_import

import os 
from azsc.transformers.AZSTransformer import AZSTransformer
from lark import Lark

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def parse(text):
    with open(os.path.join(__location__, './grammar/azsc.lark'), 'r') as f:
        grammar = f.read()

    parser = Lark(grammar)

    tree = parser.parse(text)

    t = AZSTransformer()
    t.transform(tree)
    cmd = t.get_command()

    return cmd

def test_resource_group():
    script = """
    location use 'eastus';
    group create 'test';
    """

    test = parse(script)
    assert(test) == 'az group create --name "test" --location "eastus"'

def test_storage_account():
    script = """
    location use 'eastus';
    group create 'test';
    storage account create 'teststorage' (
	    sku: 'Standard_LRS'		
    );
    """

    test = parse(script).splitlines()
    assert(test[0]) == 'az group create --name "test" --location "eastus"'
    assert(test[1]) == 'az storage account create --name "teststorage" --sku "Standard_LRS" --resource-group "test" --location "eastus"'

def test_comments():
    script = """
    # This is a comment
    """

    test = parse(script)
    assert(test) == ''
  