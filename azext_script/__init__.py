# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import sys 
from knack.help_files import helps
from azure.cli.core import AzCommandsLoader
from azext_script.parser import azure_script_parse
from azext_script._constants import VERSION

helps['script'] = """
    type: group
    short-summary: run Azure Script files.
    long-summary: |
                  Review the extension documentation learn how to create Azure Script files
                  https://github.com/yorek/azure-script
"""

helps['script run'] = """
    type: command
    short-summary: run Azure Script files.
"""

def run_script(script, target="az", output=None):
    result = azure_script_parse(script, target, output)
    if (output is None):
        print(result)

# AZ CLI Extension Entry Class
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

# Used to debug from VS Code only
if (__name__ == "__main__"):
    script = sys.argv[1]
    target = "az"
    output = None

    if len(sys.argv) >= 3: 
        target = sys.argv[2]
    
    if len(sys.argv) >= 4:
        output = sys.argv[3]
        
    run_script(script, target, output)
