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

    {normal} DEBUG:root:debug
    {green} INFO:root:info
    {bright red} CRITICAL:root:terminate

the final output is never reached as critical will trigger a shutdown.
