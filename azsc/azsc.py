from __future__ import absolute_import

import click
import sys
from azsc.script_parser import run_parser


@click.command()
@click.argument('script')
@click.option('--target', default='az', type=click.Choice(['az', 'azsh']), help="Transpiling target. Only 'az' and 'azsh' supported at the moment.")
@click.option('--output', help="Output path. Will use console if not specified")
@click.option('--debug', is_flag=True, help="Write debug information")
def cli(script, target, output, debug):    
    result = run_parser(script, target, output, debug)
    if (output is None):
        print(result)

if __name__ == '__main__':
    cli()