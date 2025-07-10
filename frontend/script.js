const chessboard = document.getElementById('chessboard');
let selectedSquare = null; // Track the currently selected square

// Create a chessboard with alternating colors (Black and White)
// Each square is a div with a class of 'square'
function createChessboard() {
    // places the initial chess pieces on the board
    // Each piece is an image inside the square div
    const pieceLayout = {
        0: ["Black-rook", "Black-knight", "Black-bishop", "Black-queen", "Black-king", "Black-bishop", "Black-knight", "Black-rook"],
        1: Array(8).fill("Black-pawn"),
        6: Array(8).fill("White-pawn"),
        7: ["White-rook", "White-knight", "White-bishop", "White-queen", "White-king", "White-bishop", "White-knight", "White-rook"]
    };

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.classList.add('square');

            const isLight = (row + col) % 2 === 0;
            square.style.backgroundColor = isLight ? '#f0d9b5' : '#b58863';

            square.dataset.row = row;
            square.dataset.col = col;

            // Place initial pieces
            if (pieceLayout[row]) {
                const pieceName = pieceLayout[row][col];
                const img = document.createElement('img');
                img.src = `assets/Chess pieces/${pieceName}.png`;
                img.classList.add('piece');
                square.appendChild(img);
            }

            // 🟡 Add click event to each square
            square.addEventListener('click', () => handleSquareClick(square));

            chessboard.appendChild(square);
        }
    }
}

function handleSquareClick(square) {
    const hasPiece = square.querySelector('img');

    if (selectedSquare === null && hasPiece) {
        // First click: select square with piece
        selectedSquare = square;
        square.style.outline = '3px solid black';

    } else if (selectedSquare) {
        // Second click: move piece to new square
        const piece = selectedSquare.querySelector('img');

        if (piece) {
            square.appendChild(piece); // Move the piece image
        }

        // Clear highlight and selection
        selectedSquare.style.outline = 'none';
        selectedSquare = null;
    }
}

createChessboard();
