import yaml
from moves import reverse_moves

setup_moves = yaml.load(open('setup_moves.yaml', 'r').read(), Loader=yaml.Loader)


def get_setup_moves(position, corner_target_position='C', edge_target_position='d'):
    if corner_target_position != 'C' or edge_target_position != 'd':
        raise NotImplementedError
    else:
        return None if setup_moves[position] is None else list(setup_moves[position])


def get_reverse_setup_moves(position, corner_target_position='C', edge_target_position='d'):
    setup_move = get_setup_moves(position, corner_target_position, edge_target_position)
    return reverse_moves(setup_move) if setup_move is not None else None
