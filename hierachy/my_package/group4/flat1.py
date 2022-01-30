import click

@click.command()
def g4cmd1():
    click.echo(f'hello from {__name__}')

@click.command()
def g4cmd2():
    click.echo(f'hello from {__name__}')
