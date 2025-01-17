
import math
import random
import copy
import tkinter as tk
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor

BOARD_SIZE = 7
MAX_MOVES = 50
EMPTY = '.'
TRIANGLE = 'A' 
CIRCLE = 'H'    

def initialize_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    # 0. satır: (0,0) = A, (0,6) = H
    board[0][0] = TRIANGLE
    board[0][6] = CIRCLE
    # 2. satır: (2,0) = A, (2,6) = H
    board[2][0] = TRIANGLE
    board[2][6] = CIRCLE
    # 4. satır: (4,0) = H, (4,6) = A
    board[4][0] = CIRCLE
    board[4][6] = TRIANGLE
    # 6. satır: (6,0) = H, (6,6) = A
    board[6][0] = CIRCLE
    board[6][6] = TRIANGLE

    return board

def get_pieces(board, player):
    pieces = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == player:
                pieces.append((r,c))
    return pieces

def in_bounds(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

def move_piece(board, start, end):
    r1, c1 = start
    r2, c2 = end
    board[r2][c2] = board[r1][c1]
    board[r1][c1] = EMPTY

def is_valid_move(board, player, start, end):
    r1, c1 = start
    r2, c2 = end
    if not in_bounds(r1, c1) or not in_bounds(r2, c2):
        return False
    if board[r1][c1] != player:
        return False
    if board[r2][c2] != EMPTY:
        return False

    if (r1 == r2 and abs(c1 - c2) == 1) or (c1 == c2 and abs(r1 - r2) == 1):
        return True
    return False

def capture_pieces(board):
    to_remove = []
   
    for r in range(BOARD_SIZE):
        row = board[r]
        start_idx = 0
        while start_idx < BOARD_SIZE:
            if row[start_idx] == EMPTY:
                start_idx += 1
                continue
            piece_type = row[start_idx]
            end_idx = start_idx
            while end_idx+1 < BOARD_SIZE and row[end_idx+1] == piece_type:
                end_idx += 1

            seg_left = start_idx-1
            seg_right = end_idx+1
            left_piece = row[seg_left] if seg_left >= 0 else None
            right_piece = row[seg_right] if seg_right < BOARD_SIZE else None

            def is_opponent(a, b):
                if b is None or b == EMPTY:
                    return False
                return b != a

            # İki uçta rakip varsa veya bir tarafta duvar(=None), diğer tarafta rakip varsa capture
            if is_opponent(piece_type, left_piece) and is_opponent(piece_type, right_piece):
                for cc in range(start_idx, end_idx+1):
                    to_remove.append((r, cc))
            elif left_piece is None and is_opponent(piece_type, right_piece):
                for cc in range(start_idx, end_idx+1):
                    to_remove.append((r, cc))
            elif is_opponent(piece_type, left_piece) and right_piece is None:
                for cc in range(start_idx, end_idx+1):
                    to_remove.append((r, cc))

            start_idx = end_idx + 1

    
    for c in range(BOARD_SIZE):
        col = [board[r][c] for r in range(BOARD_SIZE)]
        start_idx = 0
        while start_idx < BOARD_SIZE:
            if col[start_idx] == EMPTY:
                start_idx += 1
                continue
            piece_type = col[start_idx]
            end_idx = start_idx
            while end_idx+1 < BOARD_SIZE and col[end_idx+1] == piece_type:
                end_idx += 1

            top_piece = col[start_idx-1] if start_idx-1 >= 0 else None
            bottom_piece = col[end_idx+1] if end_idx+1 < BOARD_SIZE else None

            def is_opponent(a, b):
                if b is None or b == EMPTY:
                    return False
                return a != b

            if is_opponent(piece_type, top_piece) and is_opponent(piece_type, bottom_piece):
                for rr in range(start_idx, end_idx+1):
                    to_remove.append((rr,c))
            elif top_piece is None and is_opponent(piece_type, bottom_piece):
                for rr in range(start_idx, end_idx+1):
                    to_remove.append((rr,c))
            elif is_opponent(piece_type, top_piece) and bottom_piece is None:
                for rr in range(start_idx, end_idx+1):
                    to_remove.append((rr,c))
            start_idx = end_idx + 1

    to_remove = list(set(to_remove))
    for (rr, cc) in to_remove:
        board[rr][cc] = EMPTY

def check_game_end(board, move_count):
    p1_pieces = len(get_pieces(board, TRIANGLE))
    p2_pieces = len(get_pieces(board, CIRCLE))

    # İki taraf da 0 ise
    if p1_pieces == 0 and p2_pieces == 0:
        return True, "Draw"
    # AI 0, Human > 0
    elif p1_pieces == 0 and p2_pieces > 0:
        return True, "Player2 (Human) wins!"
    # Human 0, AI > 0
    elif p2_pieces == 0 and p1_pieces > 0:
        return True, "Player1 (AI) wins!"

   
    if move_count >= MAX_MOVES:
        if p1_pieces > p2_pieces:
            return True, "Player1 (AI) wins!"
        elif p2_pieces > p1_pieces:
            return True, "Player2 (Human) wins!"
        else:
            return True, "Draw"

    # İki taraf da tek taşa düştüyse
    if p1_pieces == 1 and p2_pieces == 1:
        return True, "Draw"

    return False, ""

def get_valid_moves(board, player):
    pieces = get_pieces(board, player)
    valid_moves = []
    for (r,c) in pieces:
        for (dr,dc) in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if is_valid_move(board, player, (r,c), (nr,nc)):
                valid_moves.append(((r,c),(nr,nc)))
    return valid_moves

transposition_table = {}


def evaluate_board(board):
    
    ai_count = len(get_pieces(board, TRIANGLE))
    human_count = len(get_pieces(board, CIRCLE))

    piece_difference_score = 150 * (ai_count - human_count)

    potential_capture_score = 0
    ai_moves = get_valid_moves(board, TRIANGLE)
    for move in ai_moves:
        new_board = clone_board(board)
        apply_move(new_board, move)
        new_ai_count = len(get_pieces(new_board, TRIANGLE))
        new_human_count = len(get_pieces(new_board, CIRCLE))

        if new_human_count < human_count: 
            captured = human_count - new_human_count
            potential_capture_score += captured * 5

        if new_ai_count < ai_count:      
            lost = ai_count - new_ai_count
            potential_capture_score -= lost

    sandwich_reward, sandwich_penalty = find_sandwiches(board, TRIANGLE, CIRCLE)

   
    score = (
        piece_difference_score * 200
        + sandwich_reward * 10
        - sandwich_penalty * 20
        + potential_capture_score 
    )

    return score

def find_sandwiches(board, our_piece, opp_piece):

    reward = 0
    penalty = 0
    size = len(board)

    for r in range(size):
        row = board[r]
        start_idx = 0
        while start_idx < size:
            if row[start_idx] == EMPTY:
                start_idx += 1
                continue

            piece_type = row[start_idx]
            end_idx = start_idx

            while end_idx + 1 < size and row[end_idx + 1] == piece_type:
                end_idx += 1
            
            seg_len = end_idx - start_idx + 1
            seg_left = start_idx - 1
            seg_right = end_idx + 1
            left_piece = row[seg_left] if seg_left >= 0 else None
            right_piece = row[seg_right] if seg_right < size else None

            if piece_type == our_piece:
                if left_piece == opp_piece and right_piece == opp_piece:
                    penalty += seg_len * 80
            elif piece_type == opp_piece:
                if left_piece == our_piece and right_piece == our_piece:
                    reward += seg_len * 80
            
            start_idx = end_idx + 1

   
    for c in range(size):
        col = [board[r][c] for r in range(size)]
        start_idx = 0
        while start_idx < size:
            if col[start_idx] == EMPTY:
                start_idx += 1
                continue

            piece_type = col[start_idx]
            end_idx = start_idx
            while end_idx + 1 < size and col[end_idx + 1] == piece_type:
                end_idx += 1

            seg_len = end_idx - start_idx + 1
            seg_top = start_idx - 1
            seg_bottom = end_idx + 1
            top_piece = col[seg_top] if seg_top >= 0 else None
            bottom_piece = col[seg_bottom] if seg_bottom < size else None

            if piece_type == our_piece:
                if top_piece == opp_piece and bottom_piece == opp_piece:
                    penalty += seg_len * 80
            elif piece_type == opp_piece:
                if top_piece == our_piece and bottom_piece == our_piece:
                    reward += seg_len * 80

            start_idx = end_idx + 1

    return reward, penalty


def clone_board(board):
    return [row[:] for row in board]

def apply_move(board, move):
    (start, end) = move
    move_piece(board, start, end)
    capture_pieces(board)

def minimax(board, depth, alpha, beta, maximizing_player, move_count):
    board_key = str(board)
    if board_key in transposition_table:
        return transposition_table[board_key]

    ended, result = check_game_end(board, move_count)
    if ended:
        if result == "Draw":
            return 0
        elif "AI wins" in result:
            return 1000
        else:
            return -1000

    if depth == 0:
        score = evaluate_board(board)
        transposition_table[board_key] = score
        return score

    if maximizing_player:
        max_eval = float('-inf')
        moves = get_valid_moves(board, TRIANGLE)
        for move in moves:
            new_board = clone_board(board)
            apply_move(new_board, move)
            eval_val = minimax(new_board, depth - 1, alpha, beta, False, move_count + 1)
            max_eval = max(max_eval, eval_val)
            alpha = max(alpha, eval_val)
            if beta <= alpha:
                break
        transposition_table[board_key] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        moves = get_valid_moves(board, CIRCLE)
        for move in moves:
            new_board = clone_board(board)
            apply_move(new_board, move)
            eval_val = minimax(new_board, depth - 1, alpha, beta, True, move_count + 1)
            min_eval = min(min_eval, eval_val)
            beta = min(beta, eval_val)
            if beta <= alpha:
                break
        transposition_table[board_key] = min_eval
        return min_eval

def ai_best_move(board, move_count, depth=10):

    moves = get_valid_moves(board, TRIANGLE)
    if not moves:
        return []

    ai_pieces = get_pieces(board, TRIANGLE)
    required_moves = 2 if len(ai_pieces) > 1 else 1

    if required_moves == 2:
        chosen_sets = []
        for m1 in moves:
            for m2 in moves:
                if m1 != m2 and m1[0] != m2[0]:
                    chosen_sets.append([m1, m2])
        if not chosen_sets:
            chosen_sets = [[m] for m in moves]
    else:
        chosen_sets = [[m] for m in moves]

    best_val = -math.inf
    best_move_set = random.choice(chosen_sets)

    with ThreadPoolExecutor() as executor:
        futures = []
        for move_combo in chosen_sets:
            new_board = clone_board(board)
            new_move_count = move_count
            for m in move_combo:
                apply_move(new_board, m)
                new_move_count += 1
            futures.append(executor.submit(
                minimax, new_board, depth - 1, -math.inf, math.inf, False, new_move_count
            ))

        for future, move_combo in zip(futures, chosen_sets):
            val = future.result()
            if val > best_val:
                best_val = val
                best_move_set = move_combo

    return best_move_set

##############
#  GUI Kısmı #
##############

class GameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Strategic Board Game - AI vs Human")

        self.board = initialize_board()
        self.move_count = 0

        self.selected_piece = None
        self.player_moves_made = 0
        self.required_moves = 0

       
        self.last_moved_piece_pos = None  

        self.state = "ai_turn"

 
        self.cell_size = 80
        self.frames = []

        for r in range(BOARD_SIZE):
            row_frame = []
            for c in range(BOARD_SIZE):
                canvas = tk.Canvas(
                    self.master,
                    width=self.cell_size,
                    height=self.cell_size,
                    bg="white",
                    highlightthickness=1,
                    highlightbackground="black"
                )
                canvas.bind("<Button-1>", lambda event, rr=r, cc=c: self.on_cell_click(rr, cc))
                canvas.grid(row=r, column=c)
                row_frame.append(canvas)
            self.frames.append(row_frame)

       
        self.status_label = tk.Label(self.master, text="Initializing...", font=("Arial", 14))
        self.status_label.grid(row=BOARD_SIZE, column=0, columnspan=BOARD_SIZE)

       
        self.update_board()

        
        self.master.after(500, self.play_ai_turn)

    def update_board(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                canvas = self.frames[r][c]
                canvas.delete("all") 
                piece = self.board[r][c]
                if piece == TRIANGLE:
                    
                    canvas.create_polygon(
                        self.cell_size // 2, 10,  
                        10, self.cell_size - 10, 
                        self.cell_size - 10, self.cell_size - 10,  
                        fill="red"
                    )
                elif piece == CIRCLE:           
                    canvas.create_oval(
                        10, 10,
                        self.cell_size - 10, self.cell_size - 10,
                        fill="blue"
                    )
                else:
                    canvas.create_rectangle(
                        0, 0,
                        self.cell_size, self.cell_size,
                        fill="white"
                    )

        if self.selected_piece is not None:
            sr, sc = self.selected_piece
            canvas = self.frames[sr][sc]
            canvas.create_rectangle(
                2, 2,
                self.cell_size - 2, self.cell_size - 2,
                outline="yellow", width=4
            )

    def check_end_game(self):
        ended, result = check_game_end(self.board, self.move_count)
        if ended:
            self.status_label.config(text="Game Over: " + result)
            messagebox.showinfo("Game Over", result)
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    self.frames[r][c].unbind("<Button-1>")
            return True
        return False

    def play_ai_turn(self):
        if self.check_end_game():
            return
        self.status_label.config(text="AI thinking...")
        self.master.update()
        performed = self.ai_move()
        self.move_count += performed
        self.update_board()
        if self.check_end_game():
            return
        self.state = "human_turn"
        self.prepare_human_turn()

    def prepare_human_turn(self):
        p2_pieces = get_pieces(self.board, CIRCLE)
        self.required_moves = 2 if len(p2_pieces) > 1 else 1
        self.player_moves_made = 0
        self.selected_piece = None
        self.last_moved_piece_pos = None
        self.update_board()
        self.status_label.config(
            text=f"Your turn, you must make {self.required_moves} move(s)."
        )

    def on_cell_click(self, r, c):
        if self.state != "human_turn":
            return

        piece = self.board[r][c]


        if self.selected_piece is None:
            if piece == CIRCLE:
                if self.last_moved_piece_pos is not None and (r, c) == self.last_moved_piece_pos:
                    return
                self.selected_piece = (r, c)
            else:
                return
        else:
            start = self.selected_piece
            end = (r, c)
            if is_valid_move(self.board, CIRCLE, start, end):
                move_piece(self.board, start, end)
                capture_pieces(self.board)
                self.selected_piece = None
                self.player_moves_made += 1
                self.move_count += 1
                if self.player_moves_made == 1 and self.required_moves == 2:
                    self.last_moved_piece_pos = end

                self.update_board()
                if self.check_end_game():
                    return
                if self.player_moves_made < self.required_moves:
                    kalan = self.required_moves - self.player_moves_made
                    self.status_label.config(
                        text=f"You made {self.player_moves_made} move(s), "
                             f"you must make {kalan} more."
                    )
                else:
                    self.state = "ai_turn"
                    self.master.after(500, self.play_ai_turn)
            else:
                self.selected_piece = None

        self.update_board()

    def ai_move(self):
        best_combo = ai_best_move(self.board, self.move_count, depth=6)
        performed = 0
        for m in best_combo:
            move_piece(self.board, m[0], m[1])
            performed += 1
            capture_pieces(self.board)
        return performed


def main():
    root = tk.Tk()
    game = GameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
