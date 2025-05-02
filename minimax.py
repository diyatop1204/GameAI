import copy

# 4. max_value(state, depth, alpha, beta) Function with Alpha-Beta Pruning
def max_value(current_state, depth, alpha, beta, evaluate, current_player, get_valid_moves, make_move, MIN_PLAYER, MAX_PLAYER, is_game_over):
    """Maximizing player's (MAX) value function in Minimax with Alpha-Beta pruning."""
    global state_counter
    state_counter += 1

    if is_game_over(current_state, get_valid_moves, evaluate, current_player) or depth == 0:
        return evaluate(current_state, current_player)

    max_eval = -float('inf')
    for move in get_valid_moves(current_state):
         #It ensures that modifications for simulating this move don't affect the actual game state.
        next_state =  make_move(copy_state(current_state), move[0], move[1], MAX_PLAYER)
        eval_score = min_value(next_state, depth - 1, alpha, beta, evaluate, current_player, get_valid_moves, make_move, MIN_PLAYER, MAX_PLAYER, is_game_over) # Pass alpha and beta
        max_eval = max(max_eval, eval_score)
        if max_eval >= beta: # Beta cutoff
            return max_eval
        alpha = max(alpha, max_eval)
    return max_eval

# 5. min_value(state, depth, alpha, beta) Function with Alpha-Beta Pruning
def min_value(current_state, depth, alpha, beta, evaluate, current_player, get_valid_moves, make_move, MIN_PLAYER, MAX_PLAYER, is_game_over):
    """Minimizing player's (MIN) value function in Minimax with Alpha-Beta pruning."""
    global state_counter
    state_counter += 1

    if is_game_over(current_state, get_valid_moves, evaluate, current_player) or depth == 0:
        return evaluate(current_state, current_player)

    min_eval = float('inf')
    for move in get_valid_moves(current_state):
        next_state =  make_move(copy_state(current_state), move[0], move[1], MIN_PLAYER)
        eval_score = max_value(next_state, depth - 1, alpha, beta, evaluate, current_player, get_valid_moves, make_move, MIN_PLAYER, MAX_PLAYER, is_game_over) # Pass alpha and beta
        min_eval = min(min_eval, eval_score)
        if min_eval <= alpha: # Alpha cutoff
            return min_eval
        beta = min(beta, min_eval)
    return min_eval

# 6. Get Best Move Function
def find_best_move(current_state, depth, get_valid_moves, make_move, evaluate, current_player, MAX_PLAYER, MIN_PLAYER, is_game_over):
    """Finds the best move for MAX player using Minimax with Alpha-Beta pruning."""
    global state_counter
    state_counter = 0
    best_move_row = -1
    best_move_col = -1
    max_eval = -float('inf')
    alpha = -float('inf') # Initialize alpha
    beta = float('inf')  # Initialize beta

    for move in get_valid_moves(current_state):
        next_state =  make_move(copy_state(current_state), move[0], move[1], MAX_PLAYER)
        eval_score = min_value(next_state, depth - 1, alpha, beta, evaluate, current_player, get_valid_moves, make_move, MIN_PLAYER, MAX_PLAYER, is_game_over) # Call min_value with alpha and beta

        if eval_score > max_eval:
            max_eval = eval_score
            best_move_row = move[0]
            best_move_col = move[1]
        alpha = max(alpha, max_eval) # Update alpha in the MAX context


    print(f"States searched for this move (Alpha-Beta): {state_counter}")
    return [best_move_row, best_move_col]


#Get Best Move Function for user(Min_Value)
def find_best_move_user(current_state, depth, get_valid_moves, make_move, evaluate, current_player, MAX_PLAYER, MIN_PLAYER, is_game_over):
    """Finds the best move for MAX player using Minimax with Alpha-Beta pruning."""
    global state_counter
    state_counter = 0
    best_move_row = -1
    best_move_col = -1
    min_eval = float('inf')
    alpha = -float('inf') # Initialize alpha
    beta = float('inf')  # Initialize beta

    for move in get_valid_moves(current_state):
        next_state =  make_move(copy_state(current_state), move[0], move[1], MIN_PLAYER)
        eval_score = max_value(next_state, depth - 1, alpha, beta, evaluate, current_player, get_valid_moves, make_move, MIN_PLAYER, MAX_PLAYER, is_game_over) # Call min_value with alpha and beta

        if eval_score < min_eval:
            min_eval = eval_score
            best_move_row = move[0]
            best_move_col = move[1]
        beta = min(beta, min_eval) 


    return [best_move_row, best_move_col]

# Helper function to copy the state state (for minimax simulation)
def copy_state(current_state):
    """Creates a deep copy of the game state."""
    return copy.deepcopy(current_state)



    
    