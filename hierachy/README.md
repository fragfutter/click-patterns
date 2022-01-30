# automatic command and group collection

idea is to automaticly collect commands from python package.


in the package.__init__.py (or any other module) have 

    from .click_collect import collect_commands
    cli = collect_commands()

    # and then register cli with setup.py entry_points


You can now define a command in any file using the click decorators 
click.command and click.group. They will all end up as command of the cli.

For subpackages a new command group is created. 

```
my_package/__init__.py  <- cli = collect_commands()
          /click_collect.py
          /main_command.py  <- click.Command('main1')
          /more_main_command.py  <- click.Command('main2')
          /main_group.py <- click.Group('main-group1')
          /group2/__init__.py  <- nothing here
                 /group2_command.py <- click.Command('foo')
```

will create these commands

```
cli main1
cli main2
cli main-group1 (with all subcommands you attached to it)
cli group2 foo (group2 was autocreated and foo discovered and attached)
```
