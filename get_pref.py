from flask import session


def get_pref(key):
    defaults = dict(
        pref_b_dimension=True,
        pref_s_showletter='hover',
        pref_i_shufflen=10,
        pref_s_letterscheme='european_2'
    )
    if key in session:
        return session[key]
    elif key in defaults:
        return defaults[key]
    else:
        KeyError(key)
