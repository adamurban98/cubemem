from get_pref import get_pref

english_1_letters = 'ABCDEFGHIJKLMNOPQRSTUVWX'
english_1_letters = english_1_letters + english_1_letters.lower()

european_1_letters = 'ABCDEFGHIJKLMNOPQRSTUVXZ'
european_1_letters = european_1_letters + european_1_letters.lower()

european_2_letters = 'ABCDQRSTEFGHIJKLMNOPUVXZ'
european_2_letters = european_2_letters + european_2_letters.lower()

english_2_letters = 'ABCDQRSTEFGHIJKLMNOPUVWX'
english_2_letters = english_2_letters + english_2_letters.lower()

for letters in [english_1_letters, european_1_letters, english_2_letters, english_2_letters]:
    assert len(letters) == 6*4*2

letter_schemes = dict(
    european_1={k: v for k, v in zip(european_1_letters, european_1_letters)},
    english_1={k: v for k, v in zip(european_1_letters, english_1_letters)},
    european_2={k: v for k, v in zip(european_1_letters, european_2_letters)},
    english_2={k: v for k, v in zip(european_1_letters, english_2_letters)}
)


def letter_to_user_scheme(letter):
    letter_scheme = get_pref('pref_s_letterscheme')

    letter_scheme = letter_schemes[letter_scheme]
    return letter_scheme[letter]
