const chessboard = document.getElementById('chessboard');
const notationAndAnalysis = document.getElementById('notationAndAnalysis');
let selectedSquare = null;
let currentBoard = [];
let moveHistory = [];
let saved = localStorage.getItem("chess_notation");
if (saved) {
    moveHistory = JSON.parse(saved);
}

let currentTurn = "white";


//chess pieces
function pieceTypeName(char) {
    switch (char) {
        case 'P': return 'pawn';
        case 'R': return 'rook';
        case 'N': return 'knight';
        case 'B': return 'bishop';
        case 'Q': return 'queen';
        case 'K': return 'king';
    }
}

// Create chessboard logic
function renderBoard(board) {
    chessboard.innerHTML = "";
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.classList.add('square');
            const isLight = (row + col) % 2 === 0;
            square.style.backgroundColor = isLight ? '#f0d9b5' : '#b58863';

            square.dataset.row = row;
            square.dataset.col = col;

            const pieceCode = board[row][col];
            if (pieceCode) {
                const color = pieceCode[0] === 'w' ? 'White' : 'Black';
                const type = pieceTypeName(pieceCode[1]);
                const img = document.createElement('img');
                img.src = `assets/Chess pieces/${color}-${type}.png`;
                img.classList.add('piece');
                square.appendChild(img);
            }

            square.addEventListener('click', () => handleSquareClick(square));
            chessboard.appendChild(square);
        }
    }
}

// Handle square click events and piece movement. therefore it can move the pieces
function handleSquareClick(square) {
    if (!selectedSquare && square.querySelector('img')) {
        selectedSquare = square;
        square.classList.add("selected");

    } else if (selectedSquare && square !== selectedSquare) {
        const fromRow = parseInt(selectedSquare.dataset.row);
        const fromCol = parseInt(selectedSquare.dataset.col);
        const toRow = parseInt(square.dataset.row);
        const toCol = parseInt(square.dataset.col);
        selectedSquare.classList.remove("selected");
        selectedSquare = null;
        sendMoveToBackend(fromRow, fromCol, toRow, toCol, promotion=null);
    }
}

// Communicate with backend (FASTAPI) to validate and process moves
async function sendMoveToBackend(fromRow, fromCol, toRow, toCol, promotion=null) {
    const res = await fetch("http://localhost:8000/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ from_row: fromRow, from_col: fromCol, to_row: toRow, to_col: toCol, promotion: promotion })
    });

    const result = await res.json();

    if (result.needs_promotion) {
        showPromotionUI(
            result.from[0],
            result.from[1],
            result.to[0],
            result.to[1]
        );
        return;
    }


    // Clear previous check highlights
    document.querySelectorAll('.in-check').forEach(sq => sq.classList.remove('in-check'));

    if (result.success) {
        currentBoard = result.board;
        currentTurn = result.turn;
        

        // Add move notation and analysis
        if (result.notation) {
            addNotation(result.notation);
        }

        renderBoard(currentBoard);
        updateTurnDisplay();
        displayNotation();
        
        // Highlight the opponent's king if it's in check or checkmate
        if (result.message.includes("Check")) {
            highlightKingSquare(currentTurn);
        }

        // Show check/checkmate message
        if (result.message.includes("Checkmate")) {
            highlightKingSquare(currentTurn);
            alert("Checkmate!");
        } else if (result.message.includes("Check")) {
            alert("Check!");
        }

    } else {
        alert(result.message);
    }
}

// Fetch initial board state from backend 
async function fetchBoardFromBackend() {
    const res = await fetch("http://localhost:8000/board");
    const data = await res.json();
    currentBoard = data.board;
    currentTurn = data.turn;
    renderBoard(currentBoard);
    updateTurnDisplay();
    displayNotation();
}

//checks and updates turn display (white or black)
function updateTurnDisplay() {
    const display = document.getElementById('turnDisplay');
    display.textContent = `Turn: ${currentTurn.charAt(0).toUpperCase() + currentTurn.slice(1)}`;
}

// Highlight the king's square if in check
function highlightKingSquare(color) {
    const pieces = document.querySelectorAll('img');
    for (const img of pieces) {
        if (img.src.toLowerCase().includes(`${color.toLowerCase()}-king`)) {
            img.parentElement.classList.add('in-check');
            break;
        }
    }
}

//Pawn promotion if a pawn reaches the last rank, it will prompt the user to choose a piece for promotion
function showPromotionUI(fromRow, fromCol, toRow, toCol) {
    const options = ["Q", "R", "B", "N"];

    const container = document.createElement("div");
    container.classList.add("promotion-popup");

    options.forEach(opt => {
        const btn = document.createElement("button");
        btn.textContent = opt;
        btn.onclick = () => {
            document.body.removeChild(container);
            sendMoveToBackend(fromRow, fromCol, toRow, toCol, opt);
        };
        container.appendChild(btn);
    });

    document.body.appendChild(container);
}

// Restart game functionality
document.getElementById('restartBtn').addEventListener('click', async () => {
    localStorage.removeItem("chess_notation");
    const res = await fetch("http://localhost:8000/restart", {
        method: "POST"
    });
    const result = await res.json();

    if (result.success) {
        currentBoard = result.board;
        currentTurn = result.turn;
        selectedSquare = null;
        moveHistory = [];
        document.getElementById("notationList").innerHTML = ""; // restarts the notation list
        renderBoard(currentBoard);
        updateTurnDisplay();
        displayNotation();
        alert("Game restarted!");
    }
    
});

//get the last move and highlight the squares involved in the last move
document.querySelectorAll('.last-move').forEach(sq => sq.classList.remove('last-move'));

const squares = document.querySelectorAll('.square');

squares.forEach(sq => {
    if (
        sq.dataset.row == fromRow && sq.dataset.col == fromCol ||
        sq.dataset.row == toRow && sq.dataset.col == toCol
    ) {
        sq.classList.add('last-move');
    }
});

//Add notation and analysis section
function addMoveNotationAndAnalysis( piece, from, to, isCapture, isCastling, isPromotion, promotionPiece, isCheck, isMate) {

    let notation = "";
    //castling notation
    if (isCastling) {
        notation = to === 'g1' || to === 'g8' ? "O-O" : "O-O-O";
    } else {
        let pieceSymbol = {
            pawn: "",
            rook: "R",
            knight: "N",
            bishop: "B",
            queen: "Q",
            king: "K"
        }[piece];
        
        notation += pieceSymbol;

        //capturing pieces
        if (isCapture) {
            if (piece === 'pawn') {
                notation += from[0];
            }
            notation += "x";
        }

        //Check/Checkmate notation
        notation += to;
        if (isMate) notation += "#";
        else if (isCheck) notation += "+";

        //Promotion notation
        if (isPromotion) {
            notation += "=" + promotionPiece.charAt(0).toUpperCase();
        }

    }
    // The notation will show to the list
    moveHistory.push(notation);
    displayNotation();
    console.log("Notation function called:", piece, from, to);
}

//create chess notes
function displayNotation() {
    const list = document.getElementById("notationList");
    list.innerHTML = ""; 

    for (let i = 0; i < moveHistory.length; i += 2) {
        let white = moveHistory[i] || "";
        let black = moveHistory[i + 1] || "";
        const li = document.createElement('li');
        li.textContent = `${white} ${black}`;
        list.appendChild(li);
    }
}


//Get Notation from backend and add to move history
function addNotation(notation) {
    moveHistory.push(notation);
    localStorage.setItem("chess_notation", JSON.stringify(moveHistory)); 
}

document.getElementById("saveBtn").addEventListener("click", () => {
    // if (moveHistory.length === 0) {
    //     alert("No moves to save!");
    //     return;
    // }

    let text = "";

    for (let i = 0; i < moveHistory.length; i += 2) {
        let moveNumber = Math.floor(i / 2) + 1;
        let white = moveHistory[i] || "";
        let black = moveHistory[i + 1] || "";
        text += `${moveNumber}. ${white} ${black}\n`;
    }

    const blob = new Blob([text], { type: "text/plain" });
    const link = document.createElement("a");

    link.href = URL.createObjectURL(blob);
    link.download = "chess_notation.txt";
    link.click();
});

fetchBoardFromBackend();
