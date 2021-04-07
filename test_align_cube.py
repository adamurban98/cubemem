from align_cube import get_cube_alignment_steps
from cube import Cube


def test_align_cube():
    shuffles = [
        [],
        ['X', 'X'],
        ['X'],
        ['x'],
        ['Z'],
        ['z'],
    ]

    for shuffle in shuffles:
        rotated_cube = Cube.create(shuffle=shuffle)
        alignment_steps = get_cube_alignment_steps(rotated_cube)
        assert Cube.create().cubestate_equal(rotated_cube.moves(alignment_steps))
