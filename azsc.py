from script_parser import run_parser
import click

@click.command()
@click.argument('script')
@click.option('--target', default='az', help="transpiling target. only 'az' supported at the moment.")
@click.option('--debug', is_flag=True, help="Write debug information")
def cli(script, target, debug):
    run_parser(script, target, debug)

if __name__ == '__main__':
    cli()