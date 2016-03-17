from watcher import bot_commands


def command(name, help=""):
    def decorate(f):
        bot_commands[name] = {
            "f": f,
            "help": help
        }
        return f
    return decorate
