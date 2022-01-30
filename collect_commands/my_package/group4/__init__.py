import click

@click.group()
def custom_group():
    """we wanted to have a different name, not group4"""
    # group defined here, use it
    # all commands in this module will be added to it
    pass
