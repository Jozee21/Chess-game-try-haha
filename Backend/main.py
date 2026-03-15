from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .chess_logic import get_board, get_turn, move_piece
from .chess_logic import restart_game
from .chess_logic import (
    # generate_algebraic_notation,
    global_board
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Move(BaseModel):
    from_row: int
    from_col: int
    to_row: int
    to_col: int

# api calls
@app.get("/board")
def read_board():
    return {"board": get_board(), "turn": get_turn()}

@app.post("/move")
def make_move(move: Move):
    return move_piece(move.from_row, move.from_col, move.to_row, move.to_col)

@app.post("/restart")
def restart():
    restart_game()
    return {
        "success": True,
        "board": get_board(),
        "turn": get_turn(),
        "message": "Game restarted."
    }

@app.post("/move")
def make_move(move_data: dict):
    piece = move_data["piece"]
    from_square = move_data["from"]
    to_square = move_data["to"]

    # notation = generate_algebraic_notation(
    #     piece=piece,
    #     from_square=from_square,
    #     to_square=to_square,
    #     is_capture=move_data.get("isCapture", False),
    #     is_castling=move_data.get("isCastling", False),
    #     is_promotion=move_data.get("isPromotion", False),
    #     promotion_piece=move_data.get("promotionPiece"),
    #     is_check=move_data.get("isCheck", False),
    #     is_mate=move_data.get("isMate", False)
    # )

    # return {"notation": notation}

# Run the FastAPI server with:
# uvicorn Backend.main:app --reload
# Run on TERMINAL