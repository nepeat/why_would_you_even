from basecommands import bot_commands


def command(name, help="", admin=False):
    def decorate(f):
        bot_commands[name] = {
            "f": f,
            "admin": admin,
            "help": help
        }
        return f
    return decorate
