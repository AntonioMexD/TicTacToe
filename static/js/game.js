// static/js/game.js
const squares = document.querySelectorAll('.square');
const socket = io.connect('http://127.0.0.1:5001');

squares.forEach(square => {
    square.addEventListener('click', () => {
        const index = square.getAttribute('data-index');
        socket.emit('player_move', { index: index });
    });
});

socket.on('update_board', data => {
    data.board.forEach((value, index) => {
        squares[index].textContent = value;
    });
});

socket.on('game_over', data => alert(data.winner + ' ganó!'));
