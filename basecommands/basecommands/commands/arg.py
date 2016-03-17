from basecommands.decorators import command
from basecommands.exceptions import Message
from basecommands.backends import redis


def rot(string, rot_num):
    alph = "abcdefghijklmnopqrstuvwxyz"
    outtab = alph[rot_num:] + alph[:rot_num]
    trans = str.maketrans(alph, outtab)
    return string.translate(trans)


def crypt_76543(text, method):
    rot_num = -1

    ret = ""

    for i in text:
        if i == " ":
            ret += " "
            rot_num -= 1
        else:
            ret += rot(i, rot_num % 26 if method == "encrypt" else 26 - rot_num % 26)
            rot_num -= 1

    return ret


@command("76543_encode",
    help="Encodes with the 76543 cipher."
)
def encode_76543(data=None):
    text = data["message"]["content"].split(" ", 1)[1]
    raise Message("<@%s> %s" % (data["author"]["id"], crypt_76543(text, "encrypt")))


@command("76543_decode",
    help="Decodes with the 76543 cipher."
)
def decode_76543(data=None):
    text = data["message"]["content"].split(" ", 1)[1]
    raise Message("<@%s> %s" % (data["author"]["id"], crypt_76543(text, "decode")))
