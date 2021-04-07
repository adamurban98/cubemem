
COLOR_W = 'w'
COLOR_O = 'o'


def get_cube_alignment_steps(cube):
    steps = []
    if cube.colors['TOP'] == COLOR_W:
        steps = steps + []
    elif cube.colors['BOTTOM'] == COLOR_W:
        steps = steps + ['X', 'X']
    elif cube.colors['FRONT'] == COLOR_W:
        steps = steps + ['X']
    elif cube.colors['BACK'] == COLOR_W:
        steps = steps + ['x']
    elif cube.colors['LEFT'] == COLOR_W:
        steps = steps + ['Z']
    elif cube.colors['RIGHT'] == COLOR_W:
        steps = steps + ['z']

    white_aligned_cube = cube.moves(steps)

    if white_aligned_cube.colors['FRONT'] == COLOR_O:
        steps = steps + []
    if white_aligned_cube.colors['LEFT'] == COLOR_O:
        steps = steps + ['y']
    if white_aligned_cube.colors['RIGHT'] == COLOR_O:
        steps = steps + ['Y']
    if white_aligned_cube.colors['BACK'] == COLOR_O:
        steps = steps + ['Y', 'Y']

    assert white_aligned_cube.colors['TOP'] == COLOR_W
    assert cube.moves(steps).colors['FRONT'] == COLOR_O

    return steps
