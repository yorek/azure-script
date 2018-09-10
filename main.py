from lark import Lark, Transformer

class AQLTransformer(Transformer):
    context = {}    

    def instruction(self, items):    
        #print(items)

        for item in items:
            if (item.data == 'command'):
                action = item.children[0]
            if (item.data == 'object'):
                target = item.children[0]
            if (item.data == 'subobject'):
                target2 = item.children[0]
            if (item.data == 'name'):
                name = item.children[0].strip("'")            

        if action == 'use':
            self.context[target] = name

        if action == 'create':
            location = self.context["location"]

            if target == 'resource-group':                
                print('az group {0} -n {1} -l {2} '.format(action, name, location))
            
            if target == "storage":
                resource_group = self.context["resource-group"]
                #az storage account create -n $AZURE_STORAGE_ACCOUNT -g $RESOURCE_GROUP --sku Standard_LRS
                cmd = 'az {0} {1} {2} -g {3} -n {4} -l {5} '.format(target, target2, action, resource_group, name, location)
                for param in item.children:
                    cmd += "--{0} {1}".format(param.children[0].children[0], param.children[1].children[0])
                print(cmd)



print('loading grammar...')
with open('aql2.lark', 'r') as f:
    aql_grammar = f.read()

print('loading aql file...')
with open('test2.aql', 'r') as f:
    text = f.read()

print('parsing...')
parser = Lark(aql_grammar)
tree = parser.parse(text)

print('resulting parse tree')
print(tree.pretty())
print

print('transpilation results:')
print
#AQLTransformer().transform(tree)
print
