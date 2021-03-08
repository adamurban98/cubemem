import typing

# Standard move notation       - S
# single letter Coded notation - C

_moves_capital = 'ULFRBDMESXYZ'

def _c_to_s(c):
    if c in _moves_capital:
        return c 
    else:
        return str.upper(c) + "'"

def _s_to_c(s):
    if len(s) == 1:
        return s
    else:
        return str.lower(s[0])

def list_processing_helper(s, f):
    if type(s) == str:
        s = [s]
    return [ f(x) for x in s ]

def c_to_s(c):
    return list_processing_helper(c, _c_to_s)

def s_to_c(s):
    return list_processing_helper(s, _s_to_c)
