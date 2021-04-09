from cube import Cube, DEFAULT_CUBECODE

def test_default_cube_code():
    assert Cube.create().cubecode == DEFAULT_CUBECODE

def test_moves():
    moves_one_directions = 'UDFBLRMESXYZ'
    all_moves = moves_one_directions.lower() + moves_one_directions
    for move in all_moves:
        move_reverse = move.swapcase()
        assert Cube.create().moves(move).moves(move_reverse).cubestate_equal(Cube.create())

def test_algorithms():
    '''
    Test whether an algorithm applied twice results in the original cube.
    '''

    assert Cube.create().alg_t().alg_t().cubestate_equal(Cube.create()), 'Algorithm T applied twice results in the original cube.'
    assert Cube.create().alg_y().alg_y().cubestate_equal(Cube.create()), 'Algorithm Y applied twice results in the original cube.'
    assert Cube.create().alg_r().alg_r().cubestate_equal(Cube.create()), 'Algorithm R applied twice results in the original cube.'

def test_cube_shuffled():
    assert Cube.create().cubecode == DEFAULT_CUBECODE
    assert Cube.create().shuffle  == []

    assert Cube.create().moves('URLD').shuffle == list('URLD')

    # assert Cube.create().moves('URLD').alg_t().shuffle == None
