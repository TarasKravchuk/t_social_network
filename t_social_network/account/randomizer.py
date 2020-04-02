from random import choice as ran_ch
from string import ascii_uppercase, ascii_lowercase, digits

def random_char_creator (uppercase=ascii_uppercase, lowercase=ascii_lowercase, numeric=digits, i=0, result=''):
    result += ran_ch(ran_ch((uppercase, lowercase, numeric)))
    i += 1
    if i >= 8:
        return result
    else:
        return random_char_creator(ascii_uppercase, ascii_lowercase, digits, i, result)
