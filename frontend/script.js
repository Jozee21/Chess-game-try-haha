const chessboard = document.getElementById('chessboard');

// Create a chessboard with alternating colors (Black and White)
// Each square is a div with a class of 'square'
function createChessboard() {
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.classList.add('square');

            const isLight = (row + col) % 2 === 0;
            square.style.backgroundColor = isLight ? '#f0d9b5' : '#b58863';

            square.dataset.row = row;
            square.dataset.col = col;
            chessboard.appendChild(square);
        }
    }
}

createChessboard();
