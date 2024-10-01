// static/js/game.js

let mode = '';  // Variable para almacenar el modo de juego
const squares = document.querySelectorAll('.square');
const socket = io.connect('http://127.0.0.1:5001');

// Botones de selección de modo
const vsComputerButton = document.getElementById('vs-computer');
const vsPlayerButton = document.getElementById('vs-player');
const gameBoard = document.getElementById('game-board');
const modeSelection = document.getElementById('mode-selection');
const backButton = document.getElementById('back-button');

// Manejo del botón para jugar contra la computadora
vsComputerButton.addEventListener('click', () => {
    mode = 'vs_computer';
    modeSelection.style.display = 'none';
    gameBoard.style.display = 'grid';
    backButton.style.display = 'block'; // Mostrar el botón de volver a la pantalla principal
});

// Manejo del botón para jugar contra otro jugador
vsPlayerButton.addEventListener('click', () => {
    mode = 'vs_player';
    modeSelection.style.display = 'none';
    gameBoard.style.display = 'grid';
    backButton.style.display = 'block'; // Mostrar el botón de volver a la pantalla principal
});

squares.forEach(square => {
    square.addEventListener('click', () => {
        const index = square.getAttribute('data-index');
        socket.emit('player_move', { index: index, mode: mode });
    });
});

// Volver a la pantalla principal
backButton.addEventListener('click', () => {
    gameBoard.style.display = 'none';
    modeSelection.style.display = 'block';
    backButton.style.display = 'none';
    socket.emit('restart_game');  // Reiniciar el tablero cuando vuelvas a la selección de modo
});

socket.on('update_board', data => {
    data.board.forEach((value, index) => {
        squares[index].textContent = value;
    });
});

socket.on('game_over', data => {
    alert(data.winner + ' ganó!');

    // Reiniciar el tablero automáticamente después de 2 segundos
    setTimeout(() => {
        socket.emit('restart_game');
    }, 2000);
});
