import sys
import logging
from itertools import chain

import click

try:
    import colorlog
except ImportError:
    # fail nicely so we don't depend on colorlog
    colorlog = None

"""
## colored logging setup

add the flags --debug, --quiet to the command group
and initialize logging from it.
The flags are globaly available.

Optionally activate colored output and shutdown
on critical messages.


Example:
```
@click.group(cls=LoggingGroup, color=True, critical_terminate=True)
def cli():
    pass

@cli.command()
def cmd1():
    logging.debug('debug')
    logging.info('info')
    logging.critical('terminate')
    logging.info('never reached')
```

calling it with

    cli cmd1 --debug

would produce (in normal, green, bright red)

    DEBUG:root:debug
    INFO:root:info
    CRITICAL:root:terminate

the final output is not produced as critical will trigger a shutdown.
"""

PADDED_FORMAT = '%(levelname)-10s %(name)-10s %(message)s'

class ShutdownHandler(logging.Handler):
    def emit(self, record):
        logging.shutdown()
        sys.exit(1)

class LoggingGroup(click.Group):
    """
    initialize logging.

    Args:
        color (bool): enable colored logging
        critical_terminate (bool): terminate on critical message
        fmt (str): log message format

    Default loglevel in info.

    Flag --quiet will switch to errors only

    Flag --debug will switch to debug and wins over --quiet
    """
    def __init__(self, *args,
                 color=False, critical_terminate=False,
                 fmt=logging.BASIC_FORMAT,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color
        self.critical_terminate = critical_terminate
        self.fmt = fmt
        self.params.append(
            click.Option(['--debug'], is_flag=True, default=False,
                         help='show debug messages')
        )
        self.params.append(
            click.Option(['--quiet'], is_flag=True, default=False,
                         help='show only errors')
        )

    def parse_args(self, ctx, args):
        # move debug and quiet to the beginning
        common_options = ('--debug', '--quiet')
        args = list(
            chain(
                filter(lambda x: x in common_options, args),
                filter(lambda x: x not in common_options, args),
            )
        )
        return super().parse_args(ctx, args)

    def invoke(self, ctx):
        # remove the parsed arguments from ctx so they are not passed
        # to the defined function
        debug = ctx.params.pop('debug')
        quiet = ctx.params.pop('quiet')
        self.logging_setup(debug, quiet)
        return super().invoke(ctx)

    def logging_setup(self, debug, quiet):
        logging.captureWarnings(True)
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        if quiet:
            root.setLevel(logging.ERROR)
        if debug:
            root.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(stream=sys.stderr)
        handler.setFormatter(self.logging_formatter())
        # should we iterate over root and remove all other StreamHandlers
        # connected to stderr?
        root.addHandler(handler)
        self.critical_setup()

    def logging_formatter(self):
        # default formatter
        result = logging.Formatter(self.fmt)
        if not self.color:
            return result
        if not (sys.stdout.isatty() and sys.stderr.isatty()):
            return result  # no colors for pipes
        if not colorlog:
            # send via click to stderr
            # not via logging, as this would initialize logging
            # and we would add a second stream handler
            click.echo(click.style('colorlog is not available', fg='red'), err=True)
            return result
        # we can use color
        result = colorlog.ColoredFormatter(f'%(log_color)s{self.fmt}')
        return result

    def critical_setup(self):
        if not self.critical_terminate:
            return
        root = logging.getLogger()
        root.addHandler(ShutdownHandler(level=logging.CRITICAL))
