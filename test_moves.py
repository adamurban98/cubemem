from moves import moves_to_human_readable, _match_multimoves, reverse_moves


def test_simple():
    moves_capital = 'ULFRBDMESXYZ'

    moves = list(moves_capital) + list(moves_capital.lower())

    human_readable_moves = moves_to_human_readable(moves)
    human_readable_moves_reference = (
        [move for move in moves_capital]
        + [move + '\'' for move in moves_capital]
    )

    assert human_readable_moves == human_readable_moves_reference


def test_match_multimoves():
    assert _match_multimoves(['U', 'u', 'U', 'L', 'r']) == (['U', 'u', 'U'], ['L', 'r'])
    assert _match_multimoves([]) == ([], [])
    assert _match_multimoves(['U', 'u', 'U']) == (['U', 'u', 'U'], [])
    assert _match_multimoves(['U']) == (['U'], [])


def test_double_and_triple_moves():
    assert moves_to_human_readable(list('LUUR')) == ['L', 'U2', 'R']        # UU
    assert moves_to_human_readable(list('LUuR')) == ['L', 'R']              # Uu
    assert moves_to_human_readable(list('LUuUR')) == ['L', 'U', 'R']        # UuU
    assert moves_to_human_readable(list('LUuuUR')) == ['L', 'R']            # UuuU
    assert moves_to_human_readable(list('LuuUUuuR')) == ['L', 'U2', 'R']  # uuUUuu
    assert moves_to_human_readable(list('LUUUR')) == ['L', 'U\'', 'R']        # UUU


def test_reverse():
    assert reverse_moves(list('')) == list('')
    assert reverse_moves(list('Lru')) == list('URl')
