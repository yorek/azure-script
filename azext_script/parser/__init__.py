import sys
import logging
import os 
import codecs
import pkg_resources 
from lark import Lark
from azext_script._constants import VERSION

def parse_script(script, target, output, debug):
    if (debug == True):
        logging.basicConfig(
            filename='azsc.log', 
            filemode='w', 
            level=logging.DEBUG, 
            format='%(asctime)s %(levelname)s %(message)s')
    else:
        logging.basicConfig(
            level=logging.INFO, 
            format='%(message)s')

    version = VERSION
    logging.info("az cli script compiler v {0}\n".format(version))

    logging.info("loading grammar")
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))    
    with open(os.path.join(location, os.path.join('..', 'grammar', 'azsc.lark')), 'r') as f:
        grammar = f.read()

    logging.info("loading script file")
    try:
        with open(script, 'r') as f:
            text = f.read()
    except IOError:
        error_message = "script {0} file not found".format(script)
        logging.error(error_message)
        return "ERROR: " + error_message

    logging.info("setting up parser")
    lark = Lark(grammar)

    logging.info("generating parse tree")
    tree = lark.parse(text)

    logging.debug("parse tree:\n" + tree.pretty())

    logging.info("importing parse tree transformer")
    from azext_script.transformers.AZSTransformer import AZSTransformer

    logging.info("compiling")
    t = AZSTransformer(target)
    t.transform(tree)
    cmd = t.get_command()

    if (debug==True):
        logging.debug("context:")
        ctx = t.get_context()
        for c in ctx:
            logging.debug("\t[%s]=%s", str(c), str(ctx[c]))

    logging.info("done")   

    try:
        if (output is not None):
            with codecs.open(output, "w", "utf-8") as f:
                f.write(cmd)
                f.close()
                cmd = ""                
    except OSError:
        logging.exception("unable to write to output file")
        sys.exit("unable to write to output file")

    return cmd
