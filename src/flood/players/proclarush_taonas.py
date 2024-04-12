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
        total_cells = board.get_row_count() * board.get_column_count()
        game_phase = current_flood / total_cells

        for color in valid_moves:
            temp_board = board.do_move(start_pos, color)
            flood_size = temp_board.count_flooded_cells(start_pos)

            if game_phase < 0.5:
                color_score = self.evaluate_early_game(temp_board, start_pos, color)
                color_score += self.estimate_expansion_area(temp_board, start_pos, color)
            else:
                color_score = self.evaluate_late_game(temp_board, start_pos, flood_size, opponent_start_pos)

            if color_score > best_score:
                best_score = color_score
                best_color = color

        return best_color

    def evaluate_early_game(self, board, start_pos, color):
        start_x, start_y = start_pos
        adjacent_expansion_score = 0

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = start_x + dx, start_y + dy
            if 0 <= nx < board.get_column_count() and 0 <= ny < board.get_row_count():
                if board.get_color(nx, ny) == color:
                    adjacent_expansion_score += 1

        current_flood_size = board.count_flooded_cells(start_pos)
        return current_flood_size + adjacent_expansion_score

    def estimate_expansion_area(self, board, start_pos, color):
        expansion_score = 0
        start_x, start_y = start_pos
        explored = set([start_pos])
        frontier = [(start_x + dx, start_y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

        while frontier:
            x, y = frontier.pop(0)
            if (x, y) in explored or not (0 <= x < board.get_column_count() and 0 <= y < board.get_row_count()):
                continue
            explored.add((x, y))

            if board.get_color(x, y) == color:
                expansion_score += 1
                frontier.extend([(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if (x + dx, y + dy) not in explored])

        return expansion_score


    def evaluate_late_game(self, board, start_pos, initial_flood_size, opponent_start_pos):
        subsequent_moves = board.get_valid_moves(start_pos, opponent_start_pos)
        best_future_score = initial_flood_size

        for color in subsequent_moves:
            future_board = board.do_move(start_pos, color)
            future_flood_size = future_board.count_flooded_cells(start_pos)

            if future_flood_size > best_future_score:
                best_future_score = future_flood_size

        return best_future_score
