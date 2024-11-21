import string
from random import choice

def random_string(length=10):
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(length))