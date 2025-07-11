from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .chess_logic import get_board, get_turn, move_piece

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

@app.get("/board")
def read_board():
    return {"board": get_board(), "turn": get_turn()}

@app.post("/move")
def make_move(move: Move):
    return move_piece(move.from_row, move.from_col, move.to_row, move.to_col)

# Run the FastAPI server with:
# uvicorn Backend.main:app --reload
# Run on TERMINAL