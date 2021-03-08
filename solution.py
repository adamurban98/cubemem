from cube import Cube, corner_stickers, corner_stickers, lt_sticker_to_color
from flask import url_for
from collections import OrderedDict, namedtuple
from pprint import pprint as pp

class Solution:
    @staticmethod
    def solve(cube, corner_buffer='A', edge_buffer='b'):
        solution = Solution()
        solution.corner_steps = []
        solution.corner_states = []
        solution.corner_dummy_move = []
        solution.edge_steps = []
        solution.edge_states = []
        solution.edge_dummy_move = []
        pp({ p: (cube.stickers[p], p, cube.stickers[p]==p ) for p in corner_stickers })

        # corners
        while not cube.corners_solved:
            pp({ p: (cube.stickers[p], p, cube.stickers[p]==p ) for p in corner_stickers })
            buffer_sticker = cube.stickers[corner_buffer] 
            print(cube.text)
            print(f'buffer sticker {buffer_sticker}')

            if cube.stickers[corner_buffer] in 'AER':
                print('DUMMY')
                candidates = sorted(list(set(cube.unsolved_corner_positions) - set('AER')))
                candidates += [corner_buffer] # This is the default choice
                buffer_sticker = candidates[0] 
                solution.corner_dummy_move.append(True)
            else:
                solution.corner_dummy_move.append(False)
            
            solution.corner_steps.append(buffer_sticker)
            solution.corner_states.append(cube)

            if buffer_sticker == corner_buffer:
                # This is the end, everything is already solved
                break
            
            setup = cube.setup_moves(buffer_sticker)
            swapped = setup.alg_y()
            cube = swapped.undo_setup_moves(buffer_sticker)
        
        solution.parity = len(solution.corner_steps) % 2 == 1
        if solution.parity:
            cube = cube.alg_j()

        # edges
        while not cube.edges_solved:
            buffer_sticker = cube.stickers[edge_buffer] 

            if cube.stickers[edge_buffer] in 'bm':
                print('DUMMY')
                candidates = sorted(list(set(cube.unsolved_edge_positions) - set('bm')))
                candidates += [edge_buffer] # This is the default choice
                buffer_sticker = candidates[0] 
                solution.edge_dummy_move.append(True)
            else:
                solution.edge_dummy_move.append(False)
            
            solution.edge_steps.append(buffer_sticker)
            solution.edge_states.append(cube)

            if buffer_sticker == edge_buffer:
                # This is the end, everything is already solved
                break
            
            setup = cube.setup_moves(buffer_sticker)
            swapped = setup.alg_t()
            cube = swapped.undo_setup_moves(buffer_sticker)
        

        solution.finalcube = cube

        print(cube.text)
        
        return solution


if __name__ == '__main__':
    cube = Cube().moves('B')
    print(cube.text)
    Solution.solve(cube)

    