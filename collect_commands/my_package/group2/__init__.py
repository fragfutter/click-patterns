import click

"""
define one (and only one) group that should be added to main.

In __init__ we need to manualy attach commands to it, as we
don't do autoimport from __init__

Other commands found in this module, will automaticly
attach to this group

If you don't need to specify anything for the group, see group3.
It does not define one and relies on autocreation
"""

# this group will be added to parent
@click.group()
def group2():
    """some nice message for group2"""
    pass

# including this command as we attached it
@group2.command()
def group2_cmd1():
    click.echo(f'hello from {__name__}')
    pass


# but not this command. it is not attached
# and we don't autoimport from __init__
# if you want to define a command in __init__ attach
# you must attach it yourself
@click.command()
def invisible_cmd():
    click.echo(f'hello from {__name__}')
