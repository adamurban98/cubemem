from cube_url import cube_from_url_args, cube_to_url_args
from cube import Cube

SOME_RANDOM_SHUFFLE = 'URLurl'
SOME_RANDOM_SHUFFLE_LIST = list(SOME_RANDOM_SHUFFLE)

def test_cube_from_url_args():
    cube_shuffled = Cube.create().moves(SOME_RANDOM_SHUFFLE)
    cube_cubecode = Cube.create(cube_shuffled.cubecode)

    assert {'shuffle': SOME_RANDOM_SHUFFLE} == cube_to_url_args(cube_shuffled)
    assert {'cubecode': cube_shuffled.cubecode} == cube_to_url_args(cube_cubecode)
   

def test_cube_to_url_args():
    cube_shuffled = Cube.create().moves(SOME_RANDOM_SHUFFLE)

    parsed_cube_shuffled = cube_from_url_args({'shuffle': SOME_RANDOM_SHUFFLE})
    parsed_cube_cubecode = cube_from_url_args({'cubecode': cube_shuffled.cubecode})

    assert cube_shuffled.cubestate_equal(parsed_cube_shuffled)
    assert cube_shuffled.shuffle == parsed_cube_shuffled.shuffle

    assert cube_shuffled.cubestate_equal(parsed_cube_cubecode)

import unittest
if __name__ == '__main__':
    test_cube_to_url_args()
