import click

"""these commands are collected and added at the top level"""

@click.command()
def cmd1():
    click.echo(f'hello from {__name__}')

@click.command()
def cmd2():
    click.echo(f'hello from {__name__}')
