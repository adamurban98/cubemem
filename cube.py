from functools import lru_cache
from abc import ABC, abstractmethod
import yaml
import copy
from align_cube import get_cube_alignment_steps
from setup_moves import get_setup_moves, get_reverse_setup_moves
from perms import PERM_MOVES

stickers_by_color = dict(
    w=list('abcdABCD') + ['TOP'],
    b=list('efghEFGH') + ['LEFT'],
    o=list('ijklIJKL') + ['FRONT'],
    g=list('mnopMNOP') + ['RIGHT'],
    r=list('qrstQRST') + ['BACK'],
    y=list('uvxzUVXZ') + ['BOTTOM'],
)

center_stickers = 'TOP,LEFT,RIGHT,FRONT,BACK,BOTTOM'.split(',')

letters = 'abcdefghijklmnopqrstuvxz'
edge_stickers = list(letters)
corner_stickers = list(str.upper(letters))
stickers = edge_stickers + corner_stickers + center_stickers

assert len(stickers) == 6*3*3

lt_sticker_to_color = {}
for color in stickers_by_color:
    for sticker in stickers_by_color[color]:
        lt_sticker_to_color[sticker] = color


def sorted_by_color(piece):
    return sorted(piece, key=lambda s: lt_sticker_to_color[s])


edges_raw = [
    tuple('aq'),
    tuple('bm'),
    tuple('ci'),
    tuple('de'),

    tuple('fl'),
    tuple('gz'),

    tuple('jp'),
    tuple('ku'),

    tuple('nt'),
    tuple('ov'),

    tuple('rh'),
    tuple('sx'),
]
edges = [tuple(sorted_by_color(edge)) for edge in edges_raw]

corners_raw = [
    tuple('AER'),
    tuple('BQN'),
    tuple('CMJ'),
    tuple('DIF'),

    tuple('UGL'),
    tuple('VKP'),
    tuple('XOT'),
    tuple('ZSH'),
]
corners = [tuple(sorted_by_color(corner)) for corner in corners_raw]


def piece_stickers_to_colors(piece_stickers):
    return tuple(lt_sticker_to_color[sticker] for sticker in piece_stickers)


lt_piece_colors_to_stickers = {piece_stickers_to_colors(stickers): stickers for stickers in corners+edges}

assert len(lt_piece_colors_to_stickers) == len(corners+edges)


def get_piece_colors_to_stickers_dict(piece_colors):
    if len(piece_colors) != 2 and len(piece_colors) != 3:
        raise ValueError('Piece must have 2 or 3 colors.')
    else:
        sorted_piece_colors = tuple(sorted(piece_colors))
        sorted_piece_stickers = lt_piece_colors_to_stickers.get(sorted_piece_colors, None)

        if sorted_piece_stickers is None:
            return None
        else:
            return dict(zip(sorted_piece_colors, sorted_piece_stickers))


assert get_piece_colors_to_stickers_dict(tuple('ygr')) == {'g': 'O', 'r': 'T', 'y': 'X'}
assert get_piece_colors_to_stickers_dict(tuple('wo')) == {'o': 'i', 'w': 'c'}

_corners_flattened = [item for sublist in corners for item in sublist]
assert sorted(corner_stickers) == sorted(_corners_flattened)
_edges_flattened = [item for sublist in edges for item in sublist]
assert sorted(edge_stickers) == sorted(_edges_flattened)

simple_sticker_ordering_raw = '''\
A,a,B
d,TOP,b
D,c,C
E,e,F,I,i,J,M,m,N,Q,q,R
h,LEFT,f,l,FRONT,j,p,RIGHT,n,t,BACK,r
H,g,G,L,k,K,P,o,O,T,s,S
U,u,V
z,BOTTOM,v
Z,x,X'''

simple_sticker_ordering = [row.split(',') for row in simple_sticker_ordering_raw.split('\n')]

simple_sticker_ordering_flat = [item for sublist in simple_sticker_ordering for item in sublist]


def parse_cubecode(cubecode):
    cubecode = [c for c in cubecode if c not in ',.-']
    return dict(zip(simple_sticker_ordering_flat, cubecode))


moves_config = '''
U: &moves_u
- ABCD
- QMIE
- RNJF
- abcd
- qmie
L:
- EFGH
- AIUS
- DLZR
- efgh
- dlzr
F:
- IJKL
- CPUF
- DMVG
- ijkl
- cpuf
R:
- MNOP
- JBTV
- CQXK
- mnop
- jbtv
B:
- QRST
- BEZO
- AHXN
- ahxn
- qrst
D:
- UVXZ
- KOSG
- LPTH
- uvxz
- kosg
M:
- aius
- ckxq
- [TOP,FRONT,BOTTOM,BACK]
E:
- hlpt
- fjnr
- [LEFT,FRONT,RIGHT,BACK]
S:
- dmvg
- boze
- [TOP,RIGHT,BOTTOM,LEFT]
'''

moves_config = yaml.load(moves_config, Loader=yaml.Loader)

forward_moves = {}
reverse_moves = {}

for move, configs in moves_config.items():
    submoves = []
    for config in configs:
        config = config+config
        submoves += [config[0+i:2+i] for i in range(4)]

    forward_submoves = [tuple(sm) for sm in submoves]
    reverse_submoves = [tuple(sm[::-1]) for sm in submoves]

    forward_moves[str.upper(move)] = forward_submoves
    reverse_moves[str.lower(move)] = reverse_submoves

moves = dict(**forward_moves, **reverse_moves)


DEFAULT_CUBECODE = 'wwwwwwwwwbbbooogggrrrbbbooogggrrrbbbooogggrrryyyyyyyyy'


def clean_cubecode(raw_cubecode):
    return ''.join([c for c in raw_cubecode if c in 'wbogry'])


class Cube(ABC):
    @staticmethod
    def create(cubecode=None, shuffle=None) -> 'Cube':
        if cubecode is not None and shuffle is not None:
            raise ValueError('Both cubecode and shuffle set. When using the abstract cube constructor only one of the should be set.')
        elif cubecode is not None and cubecode != DEFAULT_CUBECODE:
            return CubeCubecode(cubecode)
        elif shuffle is not None:
            return CubeShuffled(shuffle)
        else:
            return CubeShuffled([])

    @property
    def is_aligned(self):
        return get_cube_alignment_steps(self) == []

    def aligned_cube(self):
        return self.moves(get_cube_alignment_steps(self))

    @property
    @lru_cache()
    def colors(self):
        return parse_cubecode(self.cubecode)

    @property
    @lru_cache()
    def stickers(self):
        stickers = {}
        for piece in edges + corners:
            piece_colors = tuple(self.colors[position] for position in piece)
            piece_colors_to_stickers_dict = get_piece_colors_to_stickers_dict(piece_colors)
            if piece_colors_to_stickers_dict is not None:
                for position in piece:
                    stickers[position] = piece_colors_to_stickers_dict[self.colors[position]]
            else:
                print('Piece {piece} could not be parsed')
        return stickers

    @staticmethod
    def colors_to_cubecode(colors):
        cubecode = ''
        for row in simple_sticker_ordering:
            for position in row:
                cubecode += colors[position]
        return cubecode

    @abstractmethod
    def moves(self, moves):
        pass

    def alg_t(self):
        return self.moves(PERM_MOVES['T'])

    def alg_r(self):
        return self.moves(PERM_MOVES['R'])

    def alg_y(self):
        return self.moves(PERM_MOVES['Y'])

    def setup_moves(self, position):
        return self.moves(get_setup_moves(position))

    def undo_setup_moves(self, position):
        return self.moves(get_reverse_setup_moves(position))

    @abstractmethod
    def cubecode(self) -> str:
        pass

    @property
    def corners_solved(self):
        return all([self.stickers[position] == position for position in corner_stickers])

    @property
    def edges_solved(self):
        return all([self.stickers[position] == position for position in edge_stickers])

    @property
    def centers_solved(self):
        refcube = Cube.create()
        return all([refcube.colors[position] == self.colors[position] for position in center_stickers])

    @property
    def solved(self):
        return self.corners_solved and self.edges_solved and self.centers_solved

    @property
    def unsolved_corner_positions(self):
        return [p for p in corner_stickers if self.stickers[p] != p]

    @property
    def unsolved_edge_positions(self):
        return [p for p in edge_stickers if self.stickers[p] != p]

    @property
    def text(self):
        i = 0
        r = '    ' + self.cubecode[i:i+3] + '\n'
        i += 3
        r += '    ' + self.cubecode[i:i+3] + '\n'
        i += 3
        r += '    ' + self.cubecode[i:i+3] + '\n'
        i += 3
        r += self.cubecode[i:i+3] + '|' + self.cubecode[i+3:i+6] + '|' + self.cubecode[i+6:i+9] + '|' + self.cubecode[i+9:i+12] + '\n'
        i += 12
        r += self.cubecode[i:i+3] + '|' + self.cubecode[i+3:i+6] + '|' + self.cubecode[i+6:i+9] + '|' + self.cubecode[i+9:i+12] + '\n'
        i += 12
        r += self.cubecode[i:i+3] + '|' + self.cubecode[i+3:i+6] + '|' + self.cubecode[i+6:i+9] + '|' + self.cubecode[i+9:i+12] + '\n'
        i += 12
        r += '    ' + self.cubecode[i:i+3] + '\n'
        i += 3
        r += '    ' + self.cubecode[i:i+3] + '\n'
        i += 3
        r += '    ' + self.cubecode[i:i+3] + '\n'
        i += 3
        return r

    def cubestate_equal(self, other):
        return self.cubecode == other.cubecode


class CubeCubecode(Cube):
    def __init__(self, cubecode=DEFAULT_CUBECODE):
        assert len(cubecode) == 3*3*6, f'Cubecode should contain exactly {3*3*6} characters, you inserted a cubecode of length {len(cubecode)}'
        self._cubecode = cubecode

    @property
    def cubecode(self):
        return self._cubecode

    @property
    def shuffle(self):
        return None

    def move(self, move):
        new_colors = copy.deepcopy(self.colors)

        for submove in moves[move]:
            f = submove[0]
            t = submove[1]
            new_colors[t] = self.colors[f]

        return CubeCubecode(self.colors_to_cubecode(new_colors))

    def moves(self, moves):
        cube = self
        for move in moves:
            if move == 'X':
                cube = cube.moves('Rml')
            elif move == 'Y':
                cube = cube.moves('Ued')
            elif move == 'Z':
                cube = cube.moves('FSb')
            elif move == 'x':
                cube = cube.moves('rML')
            elif move == 'y':
                cube = cube.moves('uED')
            elif move == 'z':
                cube = cube.moves('fsB')
            else:
                cube = cube.move(move)
        return cube


class CubeShuffled(Cube):
    def __init__(self, shuffle=[]):
        for move in shuffle:
            valid_moves = list('UDLRFBudlrfbMESmesXYZxyz')
            assert move in valid_moves, f'Move {move} is not one of the valid moves: {valid_moves}'
        self.shuffle = shuffle

    @property
    def cubecode(self):
        return CubeCubecode().moves(self.shuffle).cubecode

    def moves(self, moves):
        return CubeShuffled(self.shuffle + list(moves))
