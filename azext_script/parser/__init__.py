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
    logger.debug("Loading grammar")    
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))    
    grammar_location = os.path.join(location, os.path.join('..', 'grammar', 'azsc.lark'))
    logger.debug("Grammar: {0}".format(grammar_location))
    try:
        with open(grammar_location, 'r') as f:
            grammar = f.read()
    except IOError:
        error_message = "Grammar '{0}' file not found".format(grammar_location)
        logger.error(error_message)
        raise(Exception(error_message))       

    logger.debug("Loading script file")
    try:
        with open(script, 'r') as f:
            text = f.read()
    except IOError:
        error_message = "Script '{0}' file not found".format(script)
        logger.error(error_message)
        raise(Exception(error_message))   

    logger.debug("Setting up parser")
    lark = Lark(grammar)

    logger.debug("Generating parse tree")
    tree = lark.parse(text)

    logger.debug("Parse tree:\n" + tree.pretty())

    logger.debug("Importing parse tree transformer")
    t = get_transformer(target)

    logger.debug("Transforming")
    t.transform(tree)
    result = t.get_result()

    logger.debug("Context:")
    ctx = t.get_context()
    for c in ctx:
        logger.debug("\t[%s]=%s", str(c), str(ctx[c]))

    logger.debug("Done")   

    try:
        if (output is not None):
            with codecs.open(output, "w", "utf-8") as f:
                f.write(result)
                f.close()
                result = ""                
    except OSError:
        error_message="unable to write to output file"
        logger.exception(error_message)
        raise(Exception(error_message))   
        
    return result
