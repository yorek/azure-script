__supported_targets = {}
__transformer = None

def register_supported_target(compiler, targets):
    for t in targets:
        print("registering target {0}->{1}".format(t, compiler))
        __supported_targets[t] = compiler

def get_supported_target(target):
    return __supported_targets[target]

def get_transformer(target):
    compiler = get_supported_target(target)
    __import__('azext_script.compilers.{0}.transformer.ScriptTransformer'.format(compiler), 'ScriptTransformer')
    return ScriptTransformer(target)
    
