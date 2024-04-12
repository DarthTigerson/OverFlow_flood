from typing import Optional
from flood.board import Board
from flood.players.base import BasePlayer

class ProclarushTaonasPlayer(BasePlayer):
    def get_best_move(
        self,
        board: Board,
        start_pos: tuple[int, int],
        opponent_start_pos: Optional[tuple[int, int]],
        timeout: Optional[float] = None,
    ) -> int:
        valid_moves = board.get_valid_moves(start_pos, opponent_start_pos)
        
        best_color = -1
        max_flood_size = -1

        for color in valid_moves:
            temp_board = board.do_move(start_pos, color)
            flood_size = temp_board.count_flooded_cells(start_pos)

            if flood_size > max_flood_size:
                max_flood_size = flood_size
                best_color = color

        return best_color