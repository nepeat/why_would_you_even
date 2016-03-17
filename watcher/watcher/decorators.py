from watcher import bot_commands


def command(name, help="", admin=False):
    def decorate(f):
        if name in bot_commands:
            raise Exception("ur dumb. (duped bot_commands name)")

        bot_commands[name] = {
            "f": f,
            "admin": admin,
            "help": help
        }
        return f
    return decorate
