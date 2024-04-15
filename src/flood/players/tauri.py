from typing import Optional
from flood.board import Board
from flood.players.base import BasePlayer
import random
from collections import defaultdict

class TauriPlayer(BasePlayer):
    def __init__(self):
        self.max_depth = 30 
        self.simulations = 200 
        self.best_global_path = None  #
        self.best_global_path_length = float('inf')
        
    def print_best_path(self, board: Board):
        if self.best_global_path is None:
            print("No best path has been stored yet.")
            return
        
        path_length = len(self.best_global_path)
        print(f"({path_length}) Current Best Path in Color:")
        for move in self.best_global_path:
            print(board.get_printed_string_for_color(move), end=" ")
        print('\n')


    def get_best_move(
        self,
        board: Board,
        start_pos: tuple[int, int],
        opponent_start_pos: Optional[tuple[int, int]] = None,
        timeout: Optional[float] = None,
    ) -> int:
        first_move_scores = defaultdict(list)
        for _ in range(self.simulations):
            path, move, is_solved = self.randomized_search(board, start_pos, opponent_start_pos, self.max_depth)
            if move is not None:
                path_length = len(path)
                first_move_scores[move].append(path_length)
                if is_solved and (self.best_global_path is None or path_length < self.best_global_path_length):
                    self.best_global_path = path
                    self.best_global_path_length = path_length
        
        if self.best_global_path:
            self.print_best_path(board)
            first_global_move = self.best_global_path[0]
            global_move_scores = first_move_scores.get(first_global_move, [])
            if global_move_scores and self.best_global_path_length <= min(global_move_scores):
                return first_global_move

        if first_move_scores:
            best_move = min(first_move_scores, key=lambda move: min(first_move_scores[move]))
            if best_move and min(first_move_scores[best_move]) < self.best_global_path_length:
                self.best_global_path = [best_move] * self.best_global_path_length
            return best_move
        
        return -1 

    def randomized_search(self, board, start_pos, opponent_start_pos, depth):
        current_board = board
        path = []
        is_solved = False

        #print(f"Starting randomized search from position: {start_pos}")  # Log the starting position

        current_color = current_board.get_color(*start_pos)
        #print(f"Starting color: {current_color}")  # Log the starting color

        for d in range(depth):
            valid_moves = list(current_board.get_valid_moves(start_pos, opponent_start_pos))
            valid_moves = [move for move in valid_moves if move != current_color]
            if not valid_moves:
                print(f"No valid moves at depth {d}")  # Log when no valid moves are available
                break

            move = random.choice(valid_moves)
            #print(f"Depth {d}: Move chosen - {move}")  # Log the chosen move

            path.append(move)
            current_board = current_board.do_move(start_pos, move)
            current_color = move  # Update the current color after making a move
            #print(f"Depth {d}: Board after move:")  # Log the board state after the move
            #current_board.print()

            if current_board.is_solved():
                is_solved = True
                #print(f"Board solved at depth {d}")  # Log when the board is solved
                break

        first_move = path[0] if path else -1
        return path, first_move, is_solved