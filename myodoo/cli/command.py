import logging
import sys
import os

import myodoo

commands = {}

class CommandType(type):
    def __init__(cls, name, bases, attrs):
        super(CommandType, cls).__init__(name, bases, attrs)
        name = getattr(cls, name, cls.__name__.lower())
        cls.name = name
        if name != 'command':
            commands[name] = cls

Command = CommandType('Command', (object,), {'run': lambda self, args: None})

class Help(Command):
    """Display the list of available commands"""
    def run(self, args):
        print('Available commands:\n')
        names = list(commands)
        for k in sorted(names):
            name = k
            doc = (commands[k].__doc__ or '').strip()
            print('    %s\t%s' % (name, doc))

def main():
    if len(sys.argv) > 1:
        args = sys.argv[1]
    else:
        args = []

    # The only shared option is '--addons-path=' needed to discover addtinoal
    # commands from modules
    if len(args) > 1 and args[0].startswith('--addons-path=') and not args[1].startswith('='):
        # parse only the addons-path, do not set the logger...
        myodoo.tools.config._parse_config([args[0]])
        args = args[1:]

    # Default legacy command
    command = 'help'

    # Subcommand discovery
    if len(args) and not args[0].startswith('-'):
        logging.disable(logging.CRITICAL)
        # TODO

        logging.disable(logging.NOTSET)
        command = args[0]
        args = args[1:]

    if command in commands:
        o = commands[command]()
        o.run(args)
    else:
        sys.exit('Unknow command %r' % (command))

main()