from cube import Cube, DEFAULT_CUBECODE

def test_default_cube_code():
    assert Cube().cubecode == DEFAULT_CUBECODE

def test_moves():
    moves_one_directions = 'UDFBLRMESXYZ'
    all_moves = moves_one_directions.lower() + moves_one_directions
    for move in all_moves:
        move_reverse = move.swapcase()
        assert Cube().moves(move).moves(move_reverse) == Cube()

def test_algorithms():
    '''
    Test whether an algorithm applied twice results in the original cube.
    '''

    assert Cube().alg_t().alg_t() == Cube(), 'Algorithm T applied twice results in the original cube.'
    assert Cube().alg_y().alg_y() == Cube(), 'Algorithm Y applied twice results in the original cube.'
    assert Cube().alg_j().alg_j() == Cube(), 'Algorithm J applied twice results in the original cube.'