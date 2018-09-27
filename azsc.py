import sys
import logging
import click
from lark import Lark

logging.basicConfig(filename='azsc.log', filemode='w', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

@click.command()
@click.argument('script')
@click.option('--target', default='az', help="transpiling target. only 'az' supported at the moment.")
@click.option('--debug', is_flag=True, help="Write debug information")
def cli(script, target, debug):
    if (debug == True):
        logging.getLogger().setLevel(logging.DEBUG)

    logging.info("AZ Script Compiler v 0.1")

    logging.info("loading grammar")
    with open('azsc.lark', 'r') as f:
        grammar = f.read()

    logging.info("loading script file")
    with open(script, 'r') as f:
        text = f.read()

    logging.info("setting up parser")
    parser = Lark(grammar)

    logging.info("generating parse tree")
    tree = parser.parse(text)

    logging.debug("parse tree:\n" + tree.pretty())

    logging.info("importing parse tree transformer")
    from transformers.AZSTransformer import AZSTransformer

    logging.info("compiling")
    t = AZSTransformer()
    t.transform(tree)
    cmd = t.get_command()

    print(cmd) 

    if (debug==True):
        logging.debug("context:")
        ctx = t.get_context()
        for c in ctx:
            logging.debug("\t[%s]=%s", str(c), str(ctx[c]))

    logging.info("done")   

if __name__ == '__main__':
    cli()