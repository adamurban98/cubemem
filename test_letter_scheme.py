from letter_scheme import letter_schemes


def test_letter_scheme():
    for letter in letter_schemes['european_1'].keys():
        assert letter_schemes['european_1'][letter] == letter


def test_english():
    for letter_scheme in [letter_schemes['english_1'], letter_schemes['english_2']]:
        letter_scheme['U'] = 'U'
        letter_scheme['V'] = 'V'
        letter_scheme['X'] = 'W'
        letter_scheme['Z'] = 'X'
        letter_scheme['u'] = 'u'
        letter_scheme['v'] = 'v'
        letter_scheme['x'] = 'w'
        letter_scheme['z'] = 'z'


def test_type2():
    for letter_scheme in [letter_schemes['english_2'], letter_schemes['european_2']]:
        letter_scheme['E'] = 'Q'
        letter_scheme['F'] = 'R'
        letter_scheme['G'] = 'S'
        letter_scheme['H'] = 'T'
        letter_scheme['e'] = 'q'
        letter_scheme['f'] = 'r'
        letter_scheme['g'] = 's'
        letter_scheme['h'] = 't'

        letter_scheme['M'] = 'I'
        letter_scheme['N'] = 'J'
        letter_scheme['O'] = 'K'
        letter_scheme['P'] = 'L'
        letter_scheme['m'] = 'i'
        letter_scheme['n'] = 'j'
        letter_scheme['o'] = 'k'
        letter_scheme['p'] = 'l'
