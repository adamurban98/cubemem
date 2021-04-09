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

        # corners
        while not cube.corners_solved:
            buffer_sticker = cube.stickers[corner_buffer]

            if cube.stickers[corner_buffer] in 'AER':
                candidates = sorted(list(set(cube.unsolved_corner_positions) - set('AER')))
                candidates += [corner_buffer]  # This is the default choice
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

        solution.state_after_corners = cube

        solution.parity = len(solution.corner_steps) % 2 == 1
        if solution.parity:
            cube = cube.alg_r()

        # edges
        while not cube.edges_solved:
            buffer_sticker = cube.stickers[edge_buffer]

            if cube.stickers[edge_buffer] in 'bm':
                candidates = sorted(list(set(cube.unsolved_edge_positions) - set('bm')))
                candidates += [edge_buffer]  # This is the default choice
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

        return solution

    def _mnemonics_pair_helper(self, step_sequence):
        length = len(step_sequence)
        for i in range(length//2):
            yield step_sequence[i*2] + step_sequence[i*2+1]

        if length % 2 == 1:
            yield step_sequence[-1]

    @property
    def corner_mnemonic_pair_ques(self):
        return self._mnemonics_pair_helper(self.corner_steps)

    @property
    def edge_mnemonic_pair_ques(self):
        return self._mnemonics_pair_helper(self.edge_steps)
