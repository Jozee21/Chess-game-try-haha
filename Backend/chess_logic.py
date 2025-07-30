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
    "wK": False, "wR0": False, "wR7": False,
    "bK": False, "bR0": False, "bR7": False
}
last_move = None

def get_board():
    return board

def get_turn():
    return turn

def find_king(color):
    target = color[0] + "K"
    for r in range(8):
        for c in range(8):
            if board[r][c] == target:
                return r, c
    return None

def is_square_attacked(row, col, color):
    enemy = "b" if color == "white" else "w"

    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            p = board[r][c]
            if p:
                if p[0] == enemy and p[1] in ("R", "Q"):
                    return True
                break
            r += dr
            c += dc

    for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            p = board[r][c]
            if p:
                if p[0] == enemy and p[1] in ("B", "Q"):
                    return True
                break
            r += dr
            c += dc

    for dr, dc in [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == enemy + "N":
                return True

    dir = -1 if color == "white" else 1
    for dc in [-1, 1]:
        r, c = row + dir, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == enemy + "P":
            return True

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == enemy + "K":
                return True

    return False

def is_in_check(color):
    king_pos = find_king(color)
    if king_pos:
        return is_square_attacked(king_pos[0], king_pos[1], color)
    return False

def is_valid_pawn_move(fr, fc, tr, tc, piece):
    dir = -1 if piece.startswith("w") else 1
    start = 6 if piece.startswith("w") else 1
    target = board[tr][tc]

    if fc == tc and tr == fr + dir and target == "":
        return True
    if fc == tc and fr == start and tr == fr + 2 * dir and board[fr + dir][fc] == "" and target == "":
        return True
    if abs(tc - fc) == 1 and tr == fr + dir and target and target[0] != piece[0]:
        return True
    # En passant
    if abs(tc - fc) == 1 and tr == fr + dir and target == "" and last_move:
        lfr, lfc, ltr, ltc, lpiece = last_move
        if lpiece[1] == "P" and abs(ltr - lfr) == 2 and ltr == fr and ltc == tc:
            return True
    return False

def is_valid_knight_move(fr, fc, tr, tc, piece):
    dr, dc = abs(tr - fr), abs(tc - fc)
    return (dr, dc) in [(2,1), (1,2)] and (board[tr][tc] == "" or board[tr][tc][0] != piece[0])

def is_valid_bishop_move(fr, fc, tr, tc, piece):
    if abs(tr - fr) != abs(tc - fc): return False
    step_r = 1 if tr > fr else -1
    step_c = 1 if tc > fc else -1
    r, c = fr + step_r, fc + step_c
    while r != tr:
        if board[r][c] != "": return False
        r += step_r
        c += step_c
    return board[tr][tc] == "" or board[tr][tc][0] != piece[0]

def is_valid_rook_move(fr, fc, tr, tc, piece):
    if fr != tr and fc != tc: return False
    if fr == tr:
        for c in range(min(fc, tc)+1, max(fc, tc)):
            if board[fr][c] != "": return False
    else:
        for r in range(min(fr, tr)+1, max(fr, tr)):
            if board[r][fc] != "": return False
    return board[tr][tc] == "" or board[tr][tc][0] != piece[0]

def is_valid_queen_move(fr, fc, tr, tc, piece):
    return is_valid_bishop_move(fr, fc, tr, tc, piece) or is_valid_rook_move(fr, fc, tr, tc, piece)

def is_valid_king_move(fr, fc, tr, tc, piece):
    return abs(fr - tr) <= 1 and abs(fc - tc) <= 1 and (board[tr][tc] == "" or board[tr][tc][0] != piece[0])

def is_valid_move(fr, fc, tr, tc, piece):
    if piece.endswith("P"):
        return is_valid_pawn_move(fr, fc, tr, tc, piece)
    if piece.endswith("N"):
        return is_valid_knight_move(fr, fc, tr, tc, piece)
    if piece.endswith("B"):
        return is_valid_bishop_move(fr, fc, tr, tc, piece)
    if piece.endswith("R"):
        return is_valid_rook_move(fr, fc, tr, tc, piece)
    if piece.endswith("Q"):
        return is_valid_queen_move(fr, fc, tr, tc, piece)
    if piece.endswith("K"):
        return is_valid_king_move(fr, fc, tr, tc, piece)
    return False

def generate_legal_moves(color):
    moves = []
    for fr in range(8):
        for fc in range(8):
            piece = board[fr][fc]
            if piece and ((color == "white" and piece.startswith("w")) or (color == "black" and piece.startswith("b"))):
                for tr in range(8):
                    for tc in range(8):
                        if is_valid_move(fr, fc, tr, tc, piece):
                            temp = board[tr][tc]
                            board[tr][tc] = piece
                            board[fr][fc] = ""
                            if not is_in_check(color):
                                moves.append((fr, fc, tr, tc))
                            board[fr][fc] = piece
                            board[tr][tc] = temp
    return moves

def is_checkmate(color):
    return is_in_check(color) and not generate_legal_moves(color)

def try_castling(fr, fc, tr, tc, piece):
    color = "white" if piece.startswith("w") else "black"
    row = fr
    king_side = tc > fc
    rook_col = 7 if king_side else 0
    rook_key = f"{piece[0]}R{rook_col}"
    king_key = f"{piece[0]}K"

    print(f"Castling check: {piece} {fr} {fc} {tr} {tc} {has_moved}")

    if has_moved.get(king_key) or has_moved.get(rook_key):
        return {"success": False, "message": "Castling not allowed. King or rook has moved."}

    step = 1 if king_side else -1
    for c in range(fc + step, rook_col, step):
        if board[row][c] != "":
            return {"success": False, "message": "Castling path is not clear."}

    for c in range(min(fc, tc), max(fc, tc)+1):
        temp = board[row][c]
        board[row][c] = piece
        board[fr][fc] = ""
        if is_in_check(color):
            board[fr][fc] = piece
            board[row][c] = temp
            return {"success": False, "message": "Cannot castle through or into check."}
        board[fr][fc] = piece
        board[row][c] = temp

    board[tr][tc] = piece
    board[fr][fc] = ""
    rook_new_col = fc + 1 if king_side else fc - 1
    board[row][rook_new_col] = board[row][rook_col]
    board[row][rook_col] = ""

    has_moved[king_key] = True
    has_moved[rook_key] = True

    return {"success": True, "message": "Castling executed!"}

def move_piece(fr, fc, tr, tc):
    global turn, last_move
    piece = board[fr][fc]
    if not piece:
        return {"success": False, "message": "No piece at source."}
    if (turn == "white" and piece[0] != "w") or (turn == "black" and piece[0] != "b"):
        return {"success": False, "message": f"It is {turn}'s turn."}

    if piece.endswith("K") and abs(fc - tc) == 2 and fr == tr:
        result = try_castling(fr, fc, tr, tc, piece)
        if result["success"]:
            turn = "black" if turn == "white" else "white"
            last_move = (fr, fc, tr, tc, piece)
            return {**result, "board": board, "turn": turn}
        else:
            return result

    if not is_valid_move(fr, fc, tr, tc, piece):
        return {"success": False, "message": f"Invalid move for {piece}."}

    target = board[tr][tc]
    board[tr][tc] = piece
    board[fr][fc] = ""

    if piece[1] == "P" and target == "" and fc != tc:
        board[fr][tc] = ""

    if is_in_check(turn):
        board[fr][fc] = piece
        board[tr][tc] = target
        return {"success": False, "message": "You cannot leave your king in check."}

    if piece == "wK":
        has_moved["wK"] = True
    elif piece == "bK":
        has_moved["bK"] = True
    elif piece == "wR" and fr == 7 and fc == 0:
        has_moved["wR0"] = True
    elif piece == "wR" and fr == 7 and fc == 7:
        has_moved["wR7"] = True
    elif piece == "bR" and fr == 0 and fc == 0:
        has_moved["bR0"] = True
    elif piece == "bR" and fr == 0 and fc == 7:
        has_moved["bR7"] = True

    last_move = (fr, fc, tr, tc, piece)
    next_turn = "black" if turn == "white" else "white"
    msg = "Move successful."
    if is_checkmate(next_turn):
        msg = "Checkmate!"
    elif is_in_check(next_turn):
        msg = "Check!"

    turn = next_turn
    return {"success": True, "board": board, "turn": turn, "message": msg}

def restart_game():
    global board, turn, has_moved, last_move
    board = [row.copy() for row in initial_board]
    turn = "white"
    has_moved = {
        "wK": False, "wR0": False, "wR7": False,
        "bK": False, "bR0": False, "bR7": False
    }
    last_move = None
