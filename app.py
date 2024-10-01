from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import game_logic

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Estado del tablero vacío
board = ['' for _ in range(9)]
current_player = 'X'

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('player_move')
def handle_player_move(data):
    global current_player

    index = int(data['index'])
    mode = data['mode']

    # Solo permite jugar si la casilla está vacía
    if board[index] == '':
        board[index] = current_player

        # Verificamos si hay un ganador
        if game_logic.check_winner(board):
            emit('game_over', {'winner': current_player}, broadcast=True)
        elif '' not in board:
            emit('game_over', {'winner': 'Empate'}, broadcast=True)
        else:
            # Alternar entre los jugadores
            if mode == 'vs_player':
                current_player = 'O' if current_player == 'X' else 'X'
            elif mode == 'vs_computer':
                # Hacer que la computadora juegue usando Minimax
                computer_move()

    emit('update_board', {'board': board}, broadcast=True)

# def computer_move():
#     best_move = game_logic.minimax(board, 'O')
#     if best_move is not None:
#         board[best_move] = 'O'
#         if game_logic.check_winner(board):
#             emit('game_over', {'winner': 'O'}, broadcast=True)
#         elif '' not in board:
#             emit('game_over', {'winner': 'Empate'}, broadcast=True)

def computer_move():
    best_move = game_logic.best_move(board, 'O')
    if best_move is not None:
        board[best_move] = 'O'
        if game_logic.check_winner(board):
            emit('game_over', {'winner': 'O'}, broadcast=True)
        elif '' not in board:
            emit('game_over', {'winner': 'Empate'}, broadcast=True)

    emit('update_board', {'board': board}, broadcast=True)

@socketio.on('restart_game')
def handle_restart_game():
    global board, current_player
    board = ['' for _ in range(9)]  # Reiniciar el tablero
    current_player = 'X'  # Reiniciar el jugador
    emit('update_board', {'board': board}, broadcast=True)  # Enviar el tablero reiniciado

if __name__ == '__main__':
    socketio.run(app, port=5001, debug=True)