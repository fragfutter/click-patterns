## common flags

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
