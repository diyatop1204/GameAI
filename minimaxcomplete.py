import copy


# max_value Function - AI:   - Creates a numerical evaluation on the move tested. (Goes through the whole game tree and the reult)
# Looks for the best moves of the AI/machine based on possible scenarios of the current state of the game without editing the actual board.  The machine does this by trying to maximise its score to win the game against the opponent.
def max_value(current_state, get_valid_moves, make_move, MIN_PLAYER, MAX_PLAYER, is_game_over, winner, player): 

    # The function checks if the current state of the game has reach a terminal node (i.e The game has ended) in the game tree. The rules of the game ending is set on each specifc game as there are different rules for winning in each game
    if is_game_over(current_state, get_valid_moves, winner, player):
        return winner(current_state, player)


    max_eval = -float('inf') #Starting evaluation value is set ton negative infinity in order for the first move of the player to be analysed as the maximum score available to be made for a base.

    #The following for loop is where moves are being tested.
    #  It checks the function 'get_valid_moves' which carry all the possible legal rules based on that specific game and current possibilities of moves based on the current state. 
    for move in get_valid_moves(current_state):
        next_state =  make_move(copy_state(current_state), move[0], move[1], MAX_PLAYER) #It ensures that modifications for simulating this move don't affect the actual game state. (Move 0 = Row, Move 1 = Sticks)
        eval_score = min_value(next_state, get_valid_moves, make_move, MIN_PLAYER, MAX_PLAYER, is_game_over, winner, player) #Mimics best possible move user can do based on machine's move
        max_eval = max(max_eval, eval_score) #Returns the 'winner' of the possible scenario by comparing the score. 

    return max_eval

#min_value Function - User
#Mimics the best possible move a user can do against a move (i.e Worst case scenario for the max player) done by the max player in the current state.
def min_value(current_state, get_valid_moves, make_move, MIN_PLAYER, MAX_PLAYER, is_game_over, winner, player):
   
    if is_game_over(current_state, get_valid_moves, winner, player):
        return winner(current_state, player)


    min_eval = float('inf')
    for move in get_valid_moves(current_state):
        next_state =  make_move(copy_state(current_state), move[0], move[1], MIN_PLAYER)
        eval_score = max_value(next_state,  get_valid_moves, make_move, MIN_PLAYER, MAX_PLAYER, is_game_over, winner, player) 
        min_eval = min(min_eval, eval_score)
    return min_eval



# Get Best Move Function
#Based on the possible moves tested out between max_value and min_value functions.
# The function identifies the best eval_score from the possible scenarios tested out and what move was made to get the result. This is what the machine will actually move.
def find_best_move(current_state, get_valid_moves, make_move,  MAX_PLAYER, MIN_PLAYER, is_game_over, winner, player):
    """Finds the best move for MAX player using Minimax with"""
    best_move_row = -1
    best_move_col = -1
    max_eval = -float('inf')

    for move in get_valid_moves(current_state):
        next_state =  make_move(copy_state(current_state), move[0], move[1], MAX_PLAYER)
        eval_score = min_value(next_state,  get_valid_moves, make_move, MIN_PLAYER, MAX_PLAYER, is_game_over, winner, player) 

        if eval_score > max_eval:
            max_eval = eval_score
            best_move_row = move[0]
            best_move_col = move[1]
       


    return [best_move_row, best_move_col] 

# Helper function to copy the state state (for minimax simulation)
def copy_state(current_state):
    """Creates a deep copy of the game state."""
    return copy.deepcopy(current_state)




# Get Best Move for user (Min_Value)
def find_best_move_user(current_state, get_valid_moves, make_move,  MAX_PLAYER, MIN_PLAYER, is_game_over, winner, player):
    1
    best_move_row = -1
    best_move_col = -1
    min_eval = float('inf')

    for move in get_valid_moves(current_state):
        next_state =  make_move(copy_state(current_state), move[0], move[1], MIN_PLAYER)
        eval_score = max_value(next_state,  get_valid_moves, make_move, MIN_PLAYER, MAX_PLAYER, is_game_over, winner, player) 

        if eval_score < min_eval:
            min_eval = eval_score
            best_move_row = move[0]
            best_move_col = move[1]
       

    return [best_move_row, best_move_col] 

    
    