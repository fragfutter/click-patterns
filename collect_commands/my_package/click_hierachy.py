import sys
import importlib
import pkgutil
import inspect

import click

"""
idea is to represent commands as a hierachy on disk
and automaticly discover them.

    program
           /part1.py
           /part2.py
           /group1/__init__.py
                  /part1.py
                  /part2.py

the collection process starts with the modules part1 and part2.
For each of these modules we check if they define a click.group. If they do we
add the group to the cli.
If no group is defined within a module, we assume that they are defining a flat
list of commands and we add all of the commands we can find inside them.

for the package group1 we expect to find one group. If no group is specified
we create one. Then we start to collect commands from group1.part1 and
group1.part2
"""

def members(module, cls):
    """yield all members of module which are subclass of cls"""
    def _filter(obj):
        try:
            return issubclass(obj.__class__, cls)
        except AttributeError:
            return False

    for _, value in inspect.getmembers(module, _filter):
        yield value



def collect_commands(parent=None, namespace=None, recursive=True):
    """iterate over namespace and collect click.commands and groups

    Args:
        parent (click.Group): add commands to this. autocreated if none is given
        namespace (module): starting point for our search, or current module
        recursive (bool): dive into pkgs we find
    Returns:
        the group with all commands added. Either the given parent or
        a fresh created one.
    """
    if namespace is None:
        module = sys.modules[__name__]
        package_name = module.__package__
        namespace = importlib.import_module(package_name)
    if parent is None:
        parent = click.Group(__name__.split('.')[-1])
    for _, name, ispkg in pkgutil.iter_modules(namespace.__path__, f'{namespace.__name__}.'):
        module = importlib.import_module(name)
        groups = list(members(module, click.Group))
        commands = list(members(module, click.Command))
        if ispkg and len(groups) == 0:
            # no group given, create one
            groups = [click.Group(name.split('.')[-1])]
        # add groups
        for group in groups:
            parent.add_command(group)
        # add commands if no group is given
        if not groups:
            for command in commands:
                parent.add_command(command)
        if ispkg and recursive:
            assert len(groups) == 1
            collect_commands(parent=groups[0], namespace=module, recursive=recursive)
    return parent
