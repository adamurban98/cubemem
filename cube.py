import string
from functools import lru_cache

stickers_by_color = dict(
    w = list('abcdABCD') + ['TOP'],
    b = list('efghEFGH') + ['LEFT'],
    o = list('ijklIJKL') + ['FRONT'],
    g = list('mnopMNOP') + ['RIGHT'],
    r = list('qrstQRST') + ['BACK'],
    y = list('uvxzUVXZ') + ['BOTTOM'],
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
from pprint import pprint as pp

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

simple_sticker_ordering_raw = \
'''A,a,B
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


import yaml
moves_config = yaml.load(moves_config)

forward_moves = {}
reverse_moves = {}

for move, configs in moves_config.items():
    submoves = []
    for config in configs:
        config = config+config
        submoves += [ config[0+i:2+i] for i in range(4) ] 
    
    forward_submoves = [tuple(sm) for sm in submoves]
    reverse_submoves = [tuple(sm[::-1]) for sm in submoves]

    forward_moves[str.upper(move)] = forward_submoves
    reverse_moves[str.lower(move)] = reverse_submoves

import copy 

moves = dict(**forward_moves, **reverse_moves)

DEFAULT_CUBECODE='wwwwwwwwwbbbooogggrrrbbbooogggrrrbbbooogggrrryyyyyyyyy'
import logging

setup_moves = yaml.load(open('setup_moves.yaml','r').read())

class Cube:
    def __init__(self, cubecode=DEFAULT_CUBECODE):
        self.set_cubecode(cubecode=cubecode)

    def set_cubecode(self, cubecode):
        cubecode = ''.join([c for c in cubecode if c not in ',.-'])
        assert len(cubecode) == 3*3*6, f'Cubecode should contain exactly {3*3*6} characters, you inserted a cubecode of length {len(cubecode)}'
        self.cubecode = cubecode

    @property
    @lru_cache
    def colors(self):
        return parse_cubecode(self.cubecode)

    @property
    @lru_cache
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
    def colors_to_cubecode(colors, sep=','):
        cubecode = ''
        for row in simple_sticker_ordering:
            for position in row:
                cubecode += colors[position]
            cubecode += sep
        return cubecode
    
    def _move(self, move):
        new_colors = copy.deepcopy(self.colors)
            
        for submove in moves[move]:
            f = submove[0]
            t = submove[1]
            new_colors[t] = self.colors[f]

        return Cube(self.colors_to_cubecode(new_colors))
                
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
                cube = cube._move(move)
        return cube
    
    def alg_y(self):
        new_colors = copy.deepcopy(self.colors)
        
        new_colors['A'] = self.colors['C']
        new_colors['C'] = self.colors['A']

        new_colors['E'] = self.colors['M']
        new_colors['M'] = self.colors['E']
        
        new_colors['R'] = self.colors['J']
        new_colors['J'] = self.colors['R']

        new_colors['a'] = self.colors['d']
        new_colors['d'] = self.colors['a']

        new_colors['q'] = self.colors['e']
        new_colors['e'] = self.colors['q']

        return Cube(self.colors_to_cubecode(new_colors))

    def setup_moves(self, position):
        return self.moves(setup_moves[position])

    def undo_setup_moves(self, position):
        return self.moves(str.swapcase(setup_moves[position][::-1]))

    @property
    def corners_solved(self):
        return all([self.stickers[position] == position for position in corner_stickers])

    @property
    def edges_solved(self):
        return all([self.stickers[position] == position for position in edge_stickers])

    @property
    def centers_solved(self):
        refcube = Cube()
        return all([refcube.colors[position] == self.colors[position] for position in center_stickers])

    @property
    def solved(self):
        return self.corners_solved and self.edges_solved and self.centers_solved
