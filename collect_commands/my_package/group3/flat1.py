import click


@click.command()
def g3cmd1():
    click.echo(f'hello from {__name__}')

@click.command()
def g3cmd2():
    click.echo(f'hello from {__name__}')
