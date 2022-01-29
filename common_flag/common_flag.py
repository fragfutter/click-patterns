from itertools import chain

import click

"""
common flags

Have an option for a CommandGroup that can be specified
anywhere on it's subcommands.

clicks default model is

   cli --debug cmd1 --cmd1-flag1
   cli --debug cmd2 --cmd2-flag1

or one would need to add the debug flag both subcommands

It would be nice to specify the debug flag anywhere
so both these calls would work

   cli cmd1 --debug --cmd1-flag1
   cli --debug cmd1 --cmd1-flag1

This contradicts clicks design decission. But for common
flags like debug, verbose, quiet it is realy nice.

See also
https://github.com/pallets/click/issues/108
"""

DEBUG = None
QUIET = None


class CommonFlag(click.Option):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help += ' (common option)'

class CommonGroup(click.Group):
    def parse_args(self, ctx, args):
        """move common_options to the beginning
        so they are parsed by the group and not by the
        subcommands"""
        # TODO define a new common_option decorator
        # collect all flags from group
        common_options = []
        for param in ctx.command.params:
            if not isinstance(param, CommonFlag):
                continue
            # this only works for flags, otherwise we need to also shift
            # arguments
            assert param.is_flag
            common_options.extend(param.opts)  # --debug
            common_options.extend(param.secondary_opts)  # --no-debug
        # reorder arguments so common_options are
        # - always at the start
        # - order is kept
        args = list(
            chain(
                filter(lambda x: x in common_options, args),
                filter(lambda x: x not in common_options, args),
            )
        )
        super().parse_args(ctx, args)
