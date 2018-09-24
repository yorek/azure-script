import sys
import logging
import click
from lark import Lark

logging.basicConfig(filename='azsc.log', level=logging.INFO, format='%(asctime)s %(message)s')

@click.command()
@click.argument('script')
@click.option('--debug', is_flag=True, help="Write debug information")
def cli(script, debug):
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

    logging.info("importing parse tree transformer")
    from transformers.AZSTransformer import AZSTransformer

    logging.info("compiling")
    t = AZSTransformer()
    t.transform(tree)
    cmd = t.get_command()

    print(cmd) 

    logging.info("done")   
