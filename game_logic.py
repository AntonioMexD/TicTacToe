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


def is_board_full(board):
    return '' not in board

def evaluate(board):
    winner = check_winner(board)
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    return 0

def alpha_beta(board, depth, is_maximizing, alpha, beta):
    score = evaluate(board)
    if score == 1 or score == -1 or is_board_full(board):
        return score

    if is_maximizing:
        max_eval = float('-inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                eval = alpha_beta(board, depth + 1, False, alpha, beta)
                board[i] = ''
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Poda beta
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'X'
                eval = alpha_beta(board, depth + 1, True, alpha, beta)
                board[i] = ''
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Poda alfa
        return min_eval

def best_move(board, player):
    best_val = float('-inf') if player == 'O' else float('inf')
    best_move = None
    for i in range(9):
        if board[i] == '':
            board[i] = player
            move_val = alpha_beta(board, 0, player == 'O', float('-inf'), float('inf'))
            board[i] = ''
            if (player == 'O' and move_val > best_val) or (player == 'X' and move_val < best_val):
                best_val = move_val
                best_move = i
    return best_move
