from typing import Optional
from flood.board import Board
from flood.players.base import BasePlayer

class ProclarushTaonasPlayer(BasePlayer):
    def get_best_move(
        self,
        board: Board,
        start_pos: tuple[int, int],
        opponent_start_pos: Optional[tuple[int, int]] = None,
        timeout: Optional[float] = None,
    ) -> int:
        valid_moves = board.get_valid_moves(start_pos, opponent_start_pos)
        
        best_color = -1
        best_score = -float('inf')

        current_flood = board.count_flooded_cells(start_pos)
        game_phase = current_flood / 10

        for color in valid_moves:
            temp_board = board.do_move(start_pos, color)
            flood_size = temp_board.count_flooded_cells(start_pos)

            if game_phase < 5:
                color_score = flood_size
            else:
                # Late game
                color_score = self.evaluate_late_game(temp_board, start_pos, flood_size, opponent_start_pos)

            if color_score > best_score:
                best_score = color_score
                best_color = color

        return best_color

    def evaluate_late_game(self, board, start_pos, initial_flood_size, opponent_start_pos):
        subsequent_moves = board.get_valid_moves(start_pos, opponent_start_pos)
        best_future_score = initial_flood_size

        for color in subsequent_moves:
            future_board = board.do_move(start_pos, color)
            future_flood_size = future_board.count_flooded_cells(start_pos)

            if future_flood_size > best_future_score:
                best_future_score = future_flood_size

        return best_future_score
