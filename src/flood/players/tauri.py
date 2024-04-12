from typing import Optional, Tuple
from flood.board import Board
from queue import PriorityQueue
from flood.players.base import BasePlayer
import time

class TauriPlayer(BasePlayer):
    def __init__(self):
        self.initial_depth = 5
        self.time_limit_per_move = 60.0

    def get_best_move(
        self,
        board: Board,
        start_pos: tuple[int, int],
        opponent_start_pos: Optional[tuple[int, int]] = None,
        timeout: Optional[float] = None,
    ) -> int:
        start_time = time.time()
        depth = self.initial_depth
        best_move = -1
        best_score = -1
        
        while time.time() - start_time < self.time_limit_per_move:
            score, move = self.lookahead_search(board, start_pos, opponent_start_pos, depth, start_time)
            if move is not None and score > best_score:
                best_score = score
                best_move = move
            depth += 1
        return best_move

    def lookahead_search(self, board, start_pos, opponent_start_pos, depth, start_time):
        if depth == 0 or board.is_solved() or time.time() - start_time > self.time_limit_per_move:
            return board.count_flooded_cells(start_pos), None

        valid_moves = board.get_valid_moves(start_pos, opponent_start_pos)
        best_color = -1
        max_score = -1

        for color in valid_moves:
            temp_board = board.do_move(start_pos, color)
            score, _ = self.lookahead_search(temp_board, start_pos, opponent_start_pos, depth - 1, start_time)
            if score > max_score:
                max_score = score
                best_color = color
        
        return max_score, best_color
