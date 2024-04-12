from typing import Optional
from flood.board import Board
from flood.players.base import BasePlayer
import random
from collections import defaultdict

class TauriPlayer(BasePlayer):
    def __init__(self):
        self.max_depth = 30
        self.simulations = 20000

    def get_best_move(
        self,
        board: Board,
        start_pos: tuple[int, int],
        opponent_start_pos: Optional[tuple[int, int]] = None,
        timeout: Optional[float] = None,
    ) -> int:
        first_move_scores = defaultdict(list)
        for _ in range(self.simulations):
            path, move = self.randomized_search(board, start_pos, opponent_start_pos, self.max_depth)
            if move is not None:
                first_move_scores[move].append(len(path))
        
        best_move = min(first_move_scores, key=lambda move: min(first_move_scores[move]))
        return best_move
    
    def randomized_search(self, board, start_pos, opponent_start_pos, depth):
        current_board = board
        path = []

        for _ in range(depth):
            valid_moves = list(current_board.get_valid_moves(start_pos, opponent_start_pos))
            if not valid_moves:
                break

            move = random.choice(valid_moves)
            path.append(move)
            current_board = current_board.do_move(start_pos, move)

            if current_board.is_solved():
                break

        first_move = path[0] if path else -1
        return path, first_move
