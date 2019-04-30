import signal
import code


def raise_keyboard_interrupt(*a):
    raise KeyboardInterrupt()


class Shell:
    def __init__(self):
        signal.signal(signal.SIGINT, raise_keyboard_interrupt)

    def console(self, local_vars):
        print("console")
        Console(locals=local_vars).interact()


class Console(code.InteractiveConsole):
    def __init__(self, locals=None, filename="<console>"):
        code.InteractiveConsole.__init__(self, locals, filename)
        try:
            import readline
            import rlcompleter
        except ImportError:
            print('readline or rlcompleter not available, autocomplete disabled.')
        else:
            readline.set_completer(rlcompleter.Completer(locals).complete)
            readline.parse_and_bind("tab: complete")
