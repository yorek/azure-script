from azext_script.compilers.Compiler import register_supported_target
from .transformer import ScriptTransformer

register_supported_target('arm', ['arm'], ScriptTransformer.ScriptTransformer)
