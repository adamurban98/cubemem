from cube import Cube
from solution import Solution

def _test_solution(cube, solution):
    assert solution.corner_states[0] == cube, 'Assert that first state is the same as the shuffled cube'

    for step in solution.corner_steps:
        cube = cube.setup_moves(step)
        cube = cube.alg_y()
        cube = cube.undo_setup_moves(step)
    
    assert (len(solution.corner_steps) % 2 == 1) == solution.parity
    assert (len(solution.edge_steps) % 2 == 1) == solution.parity

    if solution.parity:
        cube = cube.alg_j()

    for step in solution.edge_steps:
        cube = cube.setup_moves(step)
        cube = cube.alg_t()
        cube = cube.undo_setup_moves(step)

    assert cube.cubestate_equal(Cube.create()), 'Assert that the cube is solved.'

def test_solutions():
    cube1 = Cube.create().moves('URLDRB')
    solution1 = Solution.solve(cube1)
    _test_solution(cube1, solution1)
