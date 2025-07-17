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
    target = board[to_row][to_col]
    is_capture = False

    # Forward 1 step
    if from_col == to_col and to_row == from_row + direction and target == "":
        return True

    # Forward 2 steps on first move
    if (from_row == start_row and
        from_col == to_col and
        to_row == from_row + 2 * direction and
        board[from_row + direction][to_col] == "" and
        target == ""):
        return True

    # Capture diagonally
    if abs(to_col - from_col) == 1 and to_row == from_row + direction:
        if target and target[0] != piece[0]:
            return True

    return False

def is_valid_knight_move(from_row, from_col, to_row, to_col, piece):
    dr = abs(to_row - from_row)
    dc = abs(to_col - from_col)

    # Knight moves in L-shape: 2 squares in one direction and 1 square perpendicular
    if (dr == 2 and dc == 1) or (dr == 1 and dc == 2):
        target = board[to_row][to_col]
        if target == "" or target[0] != piece[0]:
            return True

    return False

def is_valid_bishop_move(from_row, from_col, to_row, to_col, piece):
    dr = abs(to_row - from_row)
    dc = abs(to_col - from_col)

    # bishop moves diagonally
    if dr != dc:
        return False

    row_step = 1 if to_row > from_row else -1
    col_step = 1 if to_col > from_col else -1

    r, c = from_row + row_step, from_col + col_step

    # Check every square between from and to — it must be empty
    while r != to_row and c != to_col:
        if board[r][c] != "":
            return False
        r += row_step
        c += col_step

    target = board[to_row][to_col]
    return target == "" or target[0] != piece[0]

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
    elif piece.endswith("N"):
        if not is_valid_knight_move(from_row, from_col, to_row, to_col, piece):
            return {"success": False, "message": "Invalid knight move."}
    elif piece.endswith("B"):
        if not is_valid_bishop_move(from_row, from_col, to_row, to_col, piece):
            return {"success": False, "message": "Invalid bishop move."}
    else:
        return {"success": False, "message": f"{piece} movement not supported yet."}

    board[to_row][to_col] = piece
    board[from_row][from_col] = ""
    turn = "black" if turn == "white" else "white"

    return {"success": True, "board": board, "turn": turn}
