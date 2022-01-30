import click

# this group will be added to parent
@click.group()
def group2():
    pass

# including this command as we attached it
@group2.command()
def group2_cmd1():
    pass


# but not this command. it is not attached
# and we don't autoimport from __init__
@click.command()
def invisible_cmd():
    # as this file has a group, only the group is imported
    # we are not attached to this group.
    pass
