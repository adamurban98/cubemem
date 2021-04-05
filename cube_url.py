from flask import url_for, request
from cube import Cube
from typing import Dict

def cube_to_url_args(cube) -> Dict[str, str]:
    if cube.shuffle is not None:
        return {'shuffle': ''.join(cube.shuffle)}
    else:
        return {'cubecode': cube.cubecode}


def cube_from_url_args(url_args):
    cubecode = url_args.get('cubecode', None)
    shuffle  = url_args.get('shuffle',  None)

    if shuffle is not None:
        return Cube.create(shuffle=list(shuffle)) 
    if cubecode is not None:
        return Cube.create(cubecode=cubecode) 
    else:
        return Cube.create()