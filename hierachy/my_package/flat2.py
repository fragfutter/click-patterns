import click

"""these functions are collected and added as top level commands"""

@click.command()
def cmd3():
    click.echo(f'hello from {__name__}')

@click.command()
def cmd4():
    click.echo(f'hello from {__name__}')
