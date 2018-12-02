import sys
import os 
import codecs
import pkg_resources 
from lark import Lark
from azext_script._constants import VERSION
from azext_script.compilers import get_transformer
from knack.log import get_logger

logger = get_logger(__name__)

def azure_script_parse(script, target, output):
    logger.debug("loading grammar")
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))    
    with open(os.path.join(location, os.path.join('..', 'grammar', 'azsc.lark')), 'r') as f:
        grammar = f.read()

    logger.debug("loading script file")
    try:
        with open(script, 'r') as f:
            text = f.read()
    except IOError:
        error_message = "script {0} file not found".format(script)
        logger.error(error_message)
        return "ERROR: " + error_message

    logger.debug("setting up parser")
    lark = Lark(grammar)

    logger.debug("generating parse tree")
    tree = lark.parse(text)

    logger.debug("parse tree:\n" + tree.pretty())

    logger.debug("importing parse tree transformer")
    t = get_transformer(target)

    logger.debug("compiling")
    #t = ScriptTransformer(target)
    t.transform(tree)
    result = t.get_result()

    # if (debug==True):
    #     logger.debug("context:")
    #     ctx = t.get_context()
    #     for c in ctx:
    #         logger.debug("\t[%s]=%s", str(c), str(ctx[c]))

    logger.debug("done")   

    try:
        if (output is not None):
            with codecs.open(output, "w", "utf-8") as f:
                f.write(result)
                f.close()
                result = ""                
    except OSError:
        logger.exception("unable to write to output file")
        sys.exit("unable to write to output file")

    return result
