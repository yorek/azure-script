# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
 
from knack.help_files import helps
from azure.cli.core import AzCommandsLoader
from azext_script.parser import azure_script_parse

helps['azure script'] = """
    type: command
    short-summary: run Azure Script files.
"""

def run_script(script, target="az", output=None):
    debug = False
    result = azure_script_parse(script, target, output, debug)
    if (output is None):
        print(result)


class AzureScriptCommandsLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType
        custom_type = CliCommandType(operations_tmpl='azext_script#{}')
        super(AzureScriptCommandsLoader, self).__init__(cli_ctx=cli_ctx,
                                                       custom_command_type=custom_type)

    def load_command_table(self, args):
        """
        Load CLI commands
        """
        with self.command_group('script') as g:
            g.custom_command('run', 'run_script')
        return self.command_table

    def load_arguments(self, _):
        """
        Load CLI Args for Knack parser
        """
        with self.argument_context('script') as c:
            c.argument('script', options_list=['--script', '-s'], help='Script to load.')
            c.argument('target', options_list=['--target', '-t'], help='Transpilation target.')
            c.argument('output', options_list=['--output-file', '-of'], help='Output file to be generated.')            
            

COMMAND_LOADER_CLS = AzureScriptCommandsLoader
