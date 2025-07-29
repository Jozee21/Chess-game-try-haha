const chessboard = document.getElementById('chessboard');
let selectedSquare = null;
let currentBoard = [];
let currentTurn = "white";

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

function handleSquareClick(square) {
    if (!selectedSquare && square.querySelector('img')) {
        selectedSquare = square;
        square.classList.add("selected");

    } else if (selectedSquare && square !== selectedSquare) {
        const fromRow = parseInt(selectedSquare.dataset.row);
        const fromCol = parseInt(selectedSquare.dataset.col);
        const toRow = parseInt(square.dataset.row);
        const toCol = parseInt(square.dataset.col);
        selectedSquare.style.outline = 'none';
        selectedSquare = null;
        sendMoveToBackend(fromRow, fromCol, toRow, toCol);
    }
}

async function sendMoveToBackend(fromRow, fromCol, toRow, toCol) {
    const res = await fetch("http://localhost:8000/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ from_row: fromRow, from_col: fromCol, to_row: toRow, to_col: toCol })
    });

    const result = await res.json();

    // Clear previous check highlights
    document.querySelectorAll('.in-check').forEach(sq => sq.classList.remove('in-check'));

    if (result.success) {
        currentBoard = result.board;
        currentTurn = result.turn;
        renderBoard(currentBoard);
        updateTurnDisplay();

        // Highlight the opponent's king if it's in check or checkmate
        if (result.message.includes("Check")) {
            const kingColor = currentTurn === "White" ? "Black" : "White";
            highlightKingSquare(kingColor);
        }

        // Show check/checkmate message
        if (result.message.includes("Checkmate")) {
            alert("Checkmate!");
        } else if (result.message.includes("Check")) {
            alert("Check!");
        }

    } else {
        alert(result.message);
    }
}


async function fetchBoardFromBackend() {
    const res = await fetch("http://localhost:8000/board");
    const data = await res.json();
    currentBoard = data.board;
    currentTurn = data.turn;
    renderBoard(currentBoard);
    updateTurnDisplay();
}

function updateTurnDisplay() {
    const display = document.getElementById('turnDisplay');
    display.textContent = `Turn: ${currentTurn.charAt(0).toUpperCase() + currentTurn.slice(1)}`;
}

function highlightKingSquare(color) {
    const pieces = document.querySelectorAll('img');
    for (const img of pieces) {
        if (img.src.toLowerCase().includes(`${color.toLowerCase()}-king`)) {
            img.parentElement.classList.add('in-check');
            break;
        }
    }
}

document.getElementById('restartBtn').addEventListener('click', async () => {
    const res = await fetch("http://localhost:8000/restart", {
        method: "POST"
    });
    const result = await res.json();

    if (result.success) {
        currentBoard = result.board;
        currentTurn = result.turn;
        selectedSquare = null;
        renderBoard(currentBoard);
        updateTurnDisplay();
        alert("Game restarted!");
    }
});

fetchBoardFromBackend();
