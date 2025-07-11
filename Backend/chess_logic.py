initial_board = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP"] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    ["wP"] * 8,
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]

board = [row.copy() for row in initial_board]
turn = "white"

def get_board():
    return board

def get_turn():
    return turn

def is_valid_pawn_move(from_row, from_col, to_row, to_col, piece):
    direction = -1 if piece.startswith("w") else 1
    start_row = 6 if piece.startswith("w") else 1

    if from_col != to_col:
        return False

    if to_row == from_row + direction and board[to_row][to_col] == "":
        return True

    if (
        from_row == start_row and
        to_row == from_row + 2 * direction and
        board[from_row + direction][to_col] == "" and
        board[to_row][to_col] == ""
    ):
        return True

    return False

def move_piece(from_row, from_col, to_row, to_col):
    global turn

    piece = board[from_row][from_col]

    if not piece:
        return {"success": False, "message": "No piece at source."}

    color = "white" if piece.startswith("w") else "black"
    if color != turn:
        return {"success": False, "message": f"It is {turn}'s turn."}

    if piece.endswith("P"):
        if not is_valid_pawn_move(from_row, from_col, to_row, to_col, piece):
            return {"success": False, "message": "Invalid pawn move."}
    else:
        return {"success": False, "message": "Only pawn moves are supported for now."}

    board[to_row][to_col] = piece
    board[from_row][from_col] = ""
    turn = "black" if turn == "white" else "white"

    return {"success": True, "board": board, "turn": turn}