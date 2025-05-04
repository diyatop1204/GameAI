from minimax import *
import copy
import time
from functools import partial

tiger_move_times = []
state = None  # Global state variable
MAX_PLAYER = 'T'  # Tiger is MAX player
MIN_PLAYER = 'D'  # Dogs are MIN player

# Setting up the board 
def game_board():
    """Initialize the game board with tigers and dogs in starting positions"""
    global state
    state = [
        ['D', 'D', 'D', 'D', 'D'],
        ['D', '.', '.', '.', 'D'],
        ['D', '.', 'T', '.', 'D'],
        ['D', '.', '.', '.', 'D'],
        ['D', 'D', 'D', 'D', 'D']
    ]

def print_state(current_state=None):
    """Prints the current state of the game."""
    if current_state is None:
        current_state = state
    print("\nCurrent Board:")
    print("   0 1 2 3 4")  # Column indices
    for i, row in enumerate(current_state):
        print(f"{i}  {' '.join(row)}")
    print()

def get_valid_moves(current_state, player=None):
    """Generates a list of valid moves for the current player (either 'T' or 'D')."""
    moves = []

    if player is None: # If player is not given
        raise ValueError("Player must be specified for get_valid_moves.")

    if player == 'T':  # Tiger's turn
        tiger_position = find_tiger(current_state)
        if tiger_position:
            r, c = tiger_position
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                          (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 5 and 0 <= nc < 5 and current_state[nr][nc] == '.':
                    moves.append(((r, c), (nr, nc)))

    elif player == 'D':  # Dog's turn
        dog_position = find_dogs(current_state)
        for r, c in dog_position:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 5 and 0 <= nc < 5 and current_state[nr][nc] == '.':
                    moves.append(((r, c), (nr, nc)))

    return moves


def evaluate(current_state, player):
    """Evaluates the game state from the perspective of the current player."""
    tiger_pos = find_tiger(current_state)
    
    # Count dogs
    dog_count = sum(row.count('D') for row in current_state)
    
    # If 6 or more dogs have been captured, tiger wins
    if dog_count <= 6:
        return 1000 if player == 'T' else -1000
    
    # If tiger doesn't exist or is trapped, dogs win
    if not tiger_pos:
        return -1000 if player == 'T' else 1000
    
    # Get valid moves for tiger
    tiger_moves = []
    r, c = tiger_pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 5 and 0 <= nc < 5 and current_state[nr][nc] == '.':
            tiger_moves.append((r, c, nr, nc))
    
    if not tiger_moves:  # Tiger is trapped
        return -1000 if player == 'T' else 1000
    
    # Otherwise, score based on number of dogs and tiger's mobility
    if player == 'T':
        return (16 - dog_count) * 100 + len(tiger_moves) * 10
    else:
        return -((16 - dog_count) * 100 + len(tiger_moves) * 10)

def make_move(current_state, start_pos, end_pos, player):
    """Makes a move on the board. Takes start_pos and end_pos as (row, col) tuples."""
    new_state = copy.deepcopy(current_state)

    start_row, start_col = start_pos
    end_row, end_col = end_pos

    # Execute the move
    piece = new_state[start_row][start_col]
    new_state[start_row][start_col] = '.'
    new_state[end_row][end_col] = piece

    if player == 'T': # removing dogs if its player T
        remove_adjacent_dogs_if_surrounded(new_state, end_row, end_col)
    
    elif piece == 'D': # Dog's move
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            mid_r, mid_c = (start_row + end_row) // 2, (start_col + end_col) // 2
            if (end_row - start_row == 2 * dr or end_row - start_row == -2 * dr) and \
               (end_col - start_col == 2 * dc or end_col - start_col == -2 * dc):
                if 0 <= mid_r < 5 and 0 <= mid_c < 5 and new_state[mid_r][mid_c] == 'T':
                    new_state[mid_r][mid_c] = '.'  # Capture the tiger
    return new_state

def is_game_over(current_state, *args):
    """Checks if the game is over."""
    # Check if 6 or more dogs have been captured
    captured_dogs = count_captured_dogs(state, current_state)
    if captured_dogs == 6:
        return True
    elif captured_dogs > 6:
        return True

    # Check if dogs have won (tiger is trapped)
    tiger_pos = find_tiger(current_state)
    if not tiger_pos:
        return True
    
    # Check if tiger has no valid moves
    r, c = tiger_pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 5 and 0 <= nc < 5 and current_state[nr][nc] == '.':
            return False  # Tiger has at least one valid move
    
    return True  # Tiger is trapped, dogs win

def get_user_move(current_state, user_choice):
    """Prompts the user for a valid move and returns the move as a tuple (start_row, start_col, end_row, end_col)."""
    valid_moves = get_valid_moves(current_state, user_choice) 
    if user_choice == 'T':
        print("Available Tiger moves:")
    else:
        print("Available Dog moves:")
    
    for i, move in enumerate(valid_moves):
        print(f"{i+1}: {user_choice} at ({move[0][0]},{move[0][1]}) to ({move[1][0]},{move[1][1]})")

    while True:
        try:
            choice = int(input(f"\nEnter the number of your chosen move (1-{len(valid_moves)}): "))
            if 1 <= choice <= len(valid_moves):
                start_pos, end_pos = valid_moves[choice - 1]
                return start_pos[0], start_pos[1], end_pos[0], end_pos[1]
            else:
                print("Invalid choice. Please enter a number between 1 and", len(valid_moves))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def find_tiger(current_state):
    """Finds the Tiger's position on the board."""
    for r in range(5):
        for c in range(5):
            if current_state[r][c] == 'T':
                return (r, c)
    return None

def find_dogs(current_state):
    """Finds all the dogs' positions on the board."""
    dog_positions = []
    for r in range(5):  
        for c in range(5):
            if current_state[r][c] == 'D':  
                dog_positions.append((r, c))
    return dog_positions

def count_captured_dogs(initial_state, current_state):
    """Count how many dogs have been captured so far"""
    initial_dogs = 16
    current_dogs = sum(row.count('D') for row in current_state)
    return initial_dogs - current_dogs

def remove_adjacent_dogs_if_surrounded(new_state, end_row, end_col):
    """Removes adjacent dogs in a straight line if they are the only two dogs in that direction."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal \
        (1, -1)   # Diagonal /
    ]

    for dr, dc in directions:
        pos1 = (end_row - dr, end_col - dc)
        pos2 = (end_row + dr, end_col + dc)

        if all(0 <= r < 5 and 0 <= c < 5 for r, c in [pos1, pos2]):
            r1, c1 = pos1
            r2, c2 = pos2

            if new_state[r1][c1] == 'D' and new_state[r2][c2] == 'D':
                # Check for any other dogs further in both directions
                # Scan in negative direction from pos1
                r_neg, c_neg = r1 - dr, c1 - dc
                while 0 <= r_neg < 5 and 0 <= c_neg < 5:
                    if new_state[r_neg][c_neg] == 'D':
                        break  # Found a third dog
                    r_neg -= dr
                    c_neg -= dc
                else:
                    # Scan in positive direction from pos2
                    r_pos, c_pos = r2 + dr, c2 + dc
                    while 0 <= r_pos < 5 and 0 <= c_pos < 5:
                        if new_state[r_pos][c_pos] == 'D':
                            break  # Found a third dog
                        r_pos += dr
                        c_pos += dc
                    else:
                        # No extra dogs found in either direction — remove both
                        new_state[r1][c1] = '.'
                        new_state[r2][c2] = '.'

# Modified minimax functions specifically for Tiger vs Dogs
def tiger_max_value(current_state, depth, alpha, beta):
    """Maximizing player's (Tiger) value function in Minimax with Alpha-Beta pruning."""
    global state_counter
    state_counter += 1

    if is_game_over(current_state) or depth == 0:
        return evaluate(current_state, 'T')

    max_eval = -float('inf')
    for move in get_valid_moves(current_state, 'T'):
        next_state = make_move(copy.deepcopy(current_state), move[0], move[1], 'T')
        eval_score = tiger_min_value(next_state, depth - 1, alpha, beta)
        max_eval = max(max_eval, eval_score)
        if max_eval >= beta:  # Beta cutoff
            return max_eval
        alpha = max(alpha, max_eval)
    return max_eval
def dog_max_value(current_state, depth, alpha, beta):
    """Maximizing player's (Dogs) value function in Minimax with Alpha-Beta pruning."""
    global state_counter
    state_counter += 1

    if is_game_over(current_state) or depth == 0:
        return evaluate(current_state, 'D')  # Use evaluation function for dogs

    max_eval = -float('inf')
    for move in get_dog_possible_moves(current_state):
        next_state = make_move(copy.deepcopy(current_state), move[0], move[1], 'D')
        eval_score = dog_min_value(next_state, depth - 1, alpha, beta)
        max_eval = max(max_eval, eval_score)
        if max_eval >= beta:  # Beta cutoff
            return max_eval
        alpha = max(alpha, max_eval)
    return max_eval

def get_tiger_possible_moves(state):
    moves = []
    for row in range(5):
        for col in range(5):
            if state[row][col] == 'T':
                # Tiger can move to adjacent spots
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                              (-1, -1), (-1, 1), (1, -1), (1, 1)]
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    # Check board boundaries
                    if 0 <= new_row < 5 and 0 <= new_col < 5:
                        if state[new_row][new_col] == '.':
                            moves.append(((row, col), (new_row, new_col)))
                        # Also check if tiger can jump over a dog
                        jump_row, jump_col = row + 2*dr, col + 2*dc
                        if 0 <= jump_row < 5 and 0 <= jump_col < 5:
                            if state[new_row][new_col] == 'D' and state[jump_row][jump_col] == '.':
                                moves.append(((row, col), (jump_row, jump_col)))
    return moves
def get_dog_possible_moves(state):
    moves = []
    for row in range(5):
        for col in range(5):
            if state[row][col] == 'D':  # If it's a dog
                # Dogs can move to adjacent spots
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                              (-1, -1), (-1, 1), (1, -1), (1, 1)]
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    # Check board boundaries
                    if 0 <= new_row < 5 and 0 <= new_col < 5:
                        if state[new_row][new_col] == '.':
                            moves.append(((row, col), (new_row, new_col)))
                        # Also check if dog can jump over a tiger
                        jump_row, jump_col = row + 2*dr, col + 2*dc
                        if 0 <= jump_row < 5 and 0 <= jump_col < 5:
                            if state[new_row][new_col] == 'T' and state[jump_row][jump_col] == '.':
                                moves.append(((row, col), (jump_row, jump_col)))
    return moves

def tiger_min_value(current_state, depth, alpha, beta):
    """Minimizing player's (Dogs) value function in Minimax with Alpha-Beta pruning."""
    global state_counter
    state_counter += 1

    if is_game_over(current_state) or depth == 0:
        return evaluate(current_state, MIN_PLAYER)

    min_eval = float('inf')
    for move in get_valid_moves(current_state, 'T'):
        next_state = make_move(copy.deepcopy(current_state), move[0], move[1], 'T')
        eval_score = tiger_max_value(next_state, depth - 1, alpha, beta)
        min_eval = min(min_eval, eval_score)
        if min_eval <= alpha:  # Alpha cutoff
            return min_eval
        beta = min(beta, min_eval)
    return min_eval
def dog_min_value(current_state, depth, alpha, beta):
    """Minimizing player's (Tiger) value function in Minimax with Alpha-Beta pruning."""
    global state_counter
    state_counter += 1

    if is_game_over(current_state) or depth == 0:
        return evaluate(current_state, MIN_PLAYER)  # Use evaluation function for tiger

    min_eval = float('inf')
    for move in get_tiger_possible_moves(current_state):
        next_state = make_move(copy.deepcopy(current_state), move[0], move[1], 'D')
        eval_score = dog_max_value(next_state, depth - 1, alpha, beta)
        min_eval = min(min_eval, eval_score)
        if min_eval <= alpha:  # Alpha cutoff
            return min_eval
        beta = min(beta, min_eval)
    return min_eval

def Tiger_vs_Dogs_main():
    global state, state_counter, user_choice
    state_counter = 0
    game_board()  # Set up the initial board
    print_state()

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Welcome to Tiger vs Dogs (Minimax with Alpha-Beta Pruning)!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    user_choice = ''
    while user_choice not in ['T', 'D']:
        user_choice = input("Do you want to play as the Tiger (T) or the Dogs (D)? ").strip().upper()
    
    user_player = user_choice
    ai_player = 'D' if user_player == 'T' else 'T'
    current_player = 'T' # Tiger always starts first
    get_valid_moves_with_player = partial(get_valid_moves, player=ai_player)
    
    depth = 3
    while True:
        try:
            depth_input = int(input("Enter the difficulty level (depth for minimax, higher means harder, e.g., 3): "))
            if depth >= 1:
                depth = depth_input
                break
        except ValueError:
            print("Invalid input. Please enter an integer depth. Using default depth 3.")
            depth = 3
            break
    print(f"Difficulty level set to depth: {depth}")

    while not is_game_over(state):
        print(f"\nIt's {current_player}'s turn.")
                
        if current_player == user_player:
            # USER'S TURN
            user_move = get_user_move(state, user_choice)
            if user_move:
                start_r, start_c, end_r, end_c = user_move
                state = make_move(state, (start_r, start_c), (end_r, end_c), current_player)
                is_game_over(state)
            else:
                print("No valid moves available for you!")
        else:
            # AI'S TURN
            print("AI is thinking...")
            start_time = time.time()

            # Flip roles 
            
            if ai_player == MIN_PLAYER:

                move = find_best_move(state, depth, get_valid_moves_with_player, make_move, evaluate,
                                    ai_player, MAX_PLAYER, MIN_PLAYER, is_game_over)
            else:
                move = find_best_move(state, depth, get_valid_moves_with_player, make_move, evaluate,
                                    ai_player, MAX_PLAYER, MIN_PLAYER, is_game_over)

            move_time = time.time() - start_time
            tiger_move_times.append(move_time)
            print(f"AI move took {move_time:.4f} seconds.")

            if move:
                (start_r, start_c), (end_r, end_c) = move
                state = make_move(state, (start_r, start_c), (end_r, end_c), ai_player)  

            else:
                print("AI has no valid moves!")
        print_state()

        # Switch player
        if current_player == 'T':
            current_player = 'D'
        else: 
            current_player = 'T'

    # Game over
    winner = "Tiger" if evaluate(state, MAX_PLAYER) > 0 else "Dogs"
    print(f"Game Over! {winner} wins!")

if __name__ == "__main__":
    Tiger_vs_Dogs_main()