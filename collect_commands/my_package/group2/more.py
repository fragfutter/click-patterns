import click

# autoattached to the group of __init__
@click.command()
def group2_more_cmd1():
    click.echo(f'hello from {__name__}')
