from lark import Lark
from transformers.AZSTransformer import AZSTransformer
import sys

def main(adl_file, debug=False):
    print('loading grammar...')
    with open('azsc.lark', 'r') as f:
        aql_grammar = f.read()

    print('loading adl file...')
    with open(adl_file, 'r') as f:
        text = f.read()

    print('parsing...')
    parser = Lark(aql_grammar)
    tree = parser.parse(text)

    if (debug):
        print('resulting parse tree')
        print(tree.pretty())
        print

    print('transpilation results:')
    print
        
    AZSTransformer().transform(tree)    
    print

def show_help():
    print("azsc <file.azs> [options]")
    print
    print("options:")
    print(" --debug : print debug info")


if __name__ == '__main__':
    debug = False

    if ( len(sys.argv) < 2 or len(sys.argv) > 3 ):
        show_help()
        exit(0)

    if (not sys.argv[1].endswith(".azs")):
        show_help()
        exit(0)
    
    if ( len(sys.argv) == 3):   
        if sys.argv[2].lower() == "--debug":
            debug = True                

    main(sys.argv[1], debug)