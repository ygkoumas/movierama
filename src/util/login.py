import random
from data.users import Users


def _set_random_key():
    global RANDOM_KEY
    RANDOM_KEY = [random.randint(-10, 10) for _ in range(100)]


def init():
    _set_random_key()


def _shift_string(word, negative=False):
    direction = -1 if negative else 1
    shifted_letters = [chr(ord(char) + direction * RANDOM_KEY[index])
                       for index, char in enumerate(word)]
    return "".join(shifted_letters)


def validate_user(username, password):
    return username in Users.get_users() and Users.get_users()[
        username] == password


def create_token(username):
    # basic encoding
    return _shift_string(username)


def _decode_token(token):
    return _shift_string(token, -1)


def validate_token(token):
    username = _decode_token(token)
    if username in Users.get_users():
        return username
    return None


def register_user(username, password):
    if username in Users.get_users():
        return False

    Users.add_user(username, password)
    return True


init()
