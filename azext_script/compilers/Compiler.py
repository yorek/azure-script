__supported_targets = {}
__available_transformers = {}
__transformer = None

def register_supported_target(compiler, targets, transformer_type):
    for t in targets:        
        #print("registering compiler->target pair: {0}->{1}".format(t, compiler))
        __supported_targets[t] = compiler
        __available_transformers[t] = transformer_type

def get_supported_target(target):
    return __supported_targets[target]

def get_transformer(target):
    #compiler = get_supported_target(target)
    #print(compiler)
    #print("importing {0} to support {1} target".format(compiler, target))
    transformer = __available_transformers[target](target)
    return transformer
    
