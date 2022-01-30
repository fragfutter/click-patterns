import click

"""
don't define any group. collect will automaticly create one for us.

but commands defined here are unreachable, we don't autocollect commands
from __init__
"""

# a default click.group will be created
# and all commands in this module will be added

# except this one, we never add commands from __init__
@click.command()
def unreachable():
    pass
