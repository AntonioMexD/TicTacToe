WIN_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
    [0, 4, 8], [2, 4, 6]              # Diagonal
]

def check_winner(board):
    for combo in WIN_COMBINATIONS:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
            return board[combo[0]]
    return None

def minimax(board, player):
    winner = check_winner(board)
    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif '' not in board:
        return 0

    if player == 'O':
        best_value = -float('inf')
        best_move = None
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                move_value = minimax(board, 'X')
                board[i] = ''
                if move_value > best_value:
                    best_value = move_value
                    best_move = i
        return best_move if best_move is not None else None
    else:
        best_value = float('inf')
        best_move = None
        for i in range(9):
            if board[i] == '':
                board[i] = 'X'
                move_value = minimax(board, 'O')
                board[i] = ''
                if move_value < best_value:
                    best_value = move_value
                    best_move = i
        return best_move if best_move is not None else None
