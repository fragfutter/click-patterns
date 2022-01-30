import click

# a default click.group will be created
# and all commands in this module will be added

# except this one, we never add commands from __init__
@click.command()
def unreachable():
    pass

