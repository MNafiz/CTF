from Crypto.Util.number import long_to_bytes
from colored import attr, fg

reset = attr(0)
yellow_fg = fg(226)
orange_fg = fg(208)

def pack(message):
    """
    Pack the message to an integer

    :param message bytes: message to hash
    """
    ret = 0
    if len(message) % 2:
        message += b'\x00'
    for ind in range(0,len(message),2):
        ret |= (message[ind] & 0xf0)
        ret |= (message[ind+1] & 0x0f)
        ret <<= 8
    return ret

def print_hash(message, hash):
    print("The hash of your message '"+ yellow_fg + "{}".format(message) + reset +  "' is : " + orange_fg  + "{}".format(hash) + reset)

def hash(message):
    """
    Make the hash of a given string

    :param message string: message to hash
    """
    packed_message = pack(message.encode())
    hash = packed_message % 2**64
    hash_str = hex(hash)[2:]
    print_hash(message,hash_str)
    return hash_str
