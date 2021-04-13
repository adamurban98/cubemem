_moves_capital = 'ULFRBDMESXYZ'


def _match_multimoves(moves):
    '''
    If given an array of moves return the longest consecutive prefix of moves that belong to and the tail.
    e.g.:
        - [U, u, U, L, R] -> [U, u, U], [L, r]
        - [] -> [], []
        - [U, U, U] -> [U, U, U], []
        - [U] -> [U], []
    '''

    if len(moves) == 0:
        return [], []
    else:
        first_move = moves[0].upper()
        for i in range(1, len(moves)+1):
            if i >= len(moves) or moves[i].upper() != first_move:
                return moves[:i], moves[i:]


def moves_to_human_readable(moves):
    assert(type(moves) == list), 'Move is not a list of chars'

    moves_processed = []
    while moves:
        multimoves, moves = _match_multimoves(moves)

        move = multimoves[0].upper()
        forward = len([move for move in multimoves if move.isupper()])
        backwards = len([move for move in multimoves if move.islower()])

        multiplier = forward - backwards
        multiplier_sign = abs(multiplier) // multiplier if multiplier != 0 else 0
        multiplier_abs = abs(multiplier) % 4

        multiplier_final = multiplier_sign * {0: 0, 1: 1, 2: 2, 3: -1}[multiplier_abs]

        if multiplier_final == 0:
            moves_processed += []
        elif multiplier_final == 1:
            moves_processed += [move]
        elif multiplier_final == 2 or multiplier_final == -2:
            moves_processed += [move + '2']
        elif multiplier_final == -1:
            moves_processed += [move + '\'']

    return moves_processed

def reverse_moves(moves):
    return [str.swapcase(move) for move in moves[::-1]]