from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import game_logic

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Inicializamos el tablero vacío
board = ['' for _ in range(9)]

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('player_move')
def handle_player_move(data):
    index = int(data['index'])
    
    # Solo permite jugar si la casilla está vacía
    if board[index] == '':
        board[index] = 'X'
        if game_logic.check_winner(board):
            emit('game_over', {'winner': 'Player'}, broadcast=True)
        else:
            computer_move()
    emit('update_board', {'board': board}, broadcast=True)

def computer_move():
    # Algoritmo Minimax para que la computadora tome su movimiento
    best_move = game_logic.minimax(board, 'O')
    if best_move is not None:
        board[best_move] = 'O'
        if game_logic.check_winner(board):
            emit('game_over', {'winner': 'Computer'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, port=5001, debug=True)