import click

# more top level commands

@click.command()
def cmd3():
    click.echo(f'hello {__name__}')

@click.command()
def cmd4():
    click.echo(f'hello {__name__}')
