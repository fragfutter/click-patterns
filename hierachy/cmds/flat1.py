import click

# top level commands

@click.command()
def cmd1():
    click.echo(f'hello {__name__}')

@click.command()
def cmd2():
    click.echo(f'hello {__name__}')
