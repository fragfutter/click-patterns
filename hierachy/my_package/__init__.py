from .click_hierachy import collect_commands

cli = collect_commands()
# or collect commands only from some subpackage
#     import my_package.define_cmds_here
#     cli = collect_commands(namespace=my_package.define_cmds_here)

# add cli as entry_point to your setup.py
