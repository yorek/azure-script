from __future__ import absolute_import

import os 
from .transformer.ScriptTransformer import ScriptTransformer
from lark import Lark

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def parse(text):
    with open(os.path.join(__location__, os.path.join('grammar', 'azsc.lark')), 'r') as f:
        grammar = f.read()

    parser = Lark(grammar)

    tree = parser.parse(text)

    t = ScriptTransformer("az")
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
    assert(test[2]) == 'az storage account create --name "teststorage" --location "eastus" --resource-group "test" --sku "Standard_LRS"'

def test_comments():
    script = """
    # This is a comment
    """

    test = parse(script)
    assert(test) == ''

def test_sqlserver():
    script = """  
    location use 'eastus';
    group create 'test';
    sql server create 'test-sqlserver' (
        admin-user: "user",
        admin-password: "password"
    );
    sql db create 'test-sqldb' (
        edition: 'Premium',
        service-objective: 'P1'
    );  
    """

    test = parse(script).splitlines()
    
    assert(test[0]) == 'az group create --name "test" --location "eastus"'
    assert(test[2]) == 'az sql server create --name "test-sqlserver" --admin-password "password" --admin-user "user" --location "eastus" --resource-group "test"'
    assert(test[4]) == 'az sql db create --name "test-sqldb" --edition "Premium" --resource-group "test" --server "test-sqlserver" --service-objective "P1"'

