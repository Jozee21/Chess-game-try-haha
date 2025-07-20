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

has_moved = {
    "wK": False,
    "wR0": False,  # a1 rook
    "wR7": False,  # h1 rook
    "bK": False,
    "bR0": False,  # a8 rook
    "bR7": False   # h8 rook
}

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

def is_valid_rook_move(from_row, from_col, to_row, to_col, piece):
    # Must move in straight line
    if from_row != to_row and from_col != to_col:
        return False

    row_step = 0
    col_step = 0

    if from_row == to_row:
        col_step = 1 if to_col > from_col else -1
    else:
        row_step = 1 if to_row > from_row else -1

    r, c = from_row + row_step, from_col + col_step

    while r != to_row or c != to_col:
        if board[r][c] != "":
            return False
        r += row_step
        c += col_step

    target = board[to_row][to_col]
    return target == "" or target[0] != piece[0]

def is_valid_queen_move(from_row, from_col, to_row, to_col, piece):
    # Queen combines rook and bishop moves
    if from_row == to_row or from_col == to_col:
        return is_valid_rook_move(from_row, from_col, to_row, to_col, piece)
    elif abs(to_row - from_row) == abs(to_col - from_col):
        return is_valid_bishop_move(from_row, from_col, to_row, to_col, piece)
    return False

def is_valid_king_move(from_row, from_col, to_row, to_col, piece):
    dr = abs(to_row - from_row)
    dc = abs(to_col - from_col)

    # Normal king move: one square
    if dr <= 1 and dc <= 1:
        target = board[to_row][to_col]
        return target == "" or target[0] != piece[0]

    # Castling conditions
    if piece == "wK" and from_row == 7 and from_col == 4 and to_row == 7:
        if to_col == 6 and not has_moved["wK"] and not has_moved["wR7"]:
            if board[7][5] == "" and board[7][6] == "":
                print("✅ Castling passed all checks:", piece, from_row, from_col, to_row, to_col)
                return "castle_kingside"
        if to_col == 2 and not has_moved["wK"] and not has_moved["wR0"]:
            if board[7][1] == "" and board[7][2] == "" and board[7][3] == "":
                return "castle_queenside"

    if piece == "bK" and from_row == 0 and from_col == 4 and to_row == 0:
        if to_col == 6 and not has_moved["bK"] and not has_moved["bR7"]:
            if board[0][5] == "" and board[0][6] == "":
                return "castle_kingside"
        if to_col == 2 and not has_moved["bK"] and not has_moved["bR0"]:
            if board[0][1] == "" and board[0][2] == "" and board[0][3] == "":
                return "castle_queenside"

    return False

def move_piece(from_row, from_col, to_row, to_col):
    global turn

    piece = board[from_row][from_col]

    # Track moved pieces for castling
    if piece == "wK":
        has_moved["wK"] = True
    elif piece == "bK":
        has_moved["bK"] = True
    elif piece == "wR" and from_row == 7:
        if from_col == 0:
            has_moved["wR0"] = True
        elif from_col == 7:
            has_moved["wR7"] = True
    elif piece == "bR" and from_row == 0:
        if from_col == 0:
            has_moved["bR0"] = True
        elif from_col == 7:
            has_moved["bR7"] = True

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
    elif piece.endswith("R"):
        if not is_valid_rook_move(from_row, from_col, to_row, to_col, piece):
            return {"success": False, "message": "Invalid rook move."}
    elif piece.endswith("Q"):
        if not is_valid_queen_move(from_row, from_col, to_row, to_col, piece):
            return {"success": False, "message": "Invalid queen move."}
    elif piece.endswith("K"):
        king_result = is_valid_king_move(from_row, from_col, to_row, to_col, piece)

        if king_result == "castle_kingside":
            board[to_row][to_col] = piece
            board[from_row][from_col] = ""
            board[to_row][to_col - 1] = board[to_row][7]  # move rook
            board[to_row][7] = ""
            has_moved[piece] = True
            if piece == "wK":
                has_moved["wR7"] = True
            else:
                has_moved["bR7"] = True

        elif king_result == "castle_queenside":
            board[to_row][to_col] = piece
            board[from_row][from_col] = ""
            board[to_row][to_col + 1] = board[to_row][0]  # move rook
            board[to_row][0] = ""
            has_moved[piece] = True
            if piece == "wK":
                has_moved["wR0"] = True
            else:
                has_moved["bR0"] = True

        elif king_result is True:
            board[to_row][to_col] = piece
            board[from_row][from_col] = ""
            has_moved[piece] = True

        else:
            return {"success": False, "message": "Invalid king move."}

    else:
            return {"success": False, "message": f"{piece} movement not supported."}

    board[to_row][to_col] = piece
    board[from_row][from_col] = ""
    turn = "black" if turn == "white" else "white"

    return {"success": True, "board": board, "turn": turn}
