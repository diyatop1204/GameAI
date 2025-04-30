from minimax import *
import copy
import time

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

    # Infer the player if it's not given
    if player is None:
        # Count T and D to guess whose turn it is
        flat = sum(current_state, [])  # Flatten the board
        tiger_count = flat.count('T')
        dog_count = flat.count('D')

        # Basic heuristic: if dogs > tigers, it's dog's turn
        player = 'D' if dog_count > tiger_count else 'T'

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
    
    # If 10 or more dogs have been captured, tiger wins
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

    # If it's the tiger's move, check for captures
    if piece == 'T':
        # Check in all 8 directions for potential captures
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            mid_r, mid_c = (start_row + end_row) // 2, (start_col + end_col) // 2
            if (end_row - start_row == 2 * dr or end_row - start_row == -2 * dr) and \
               (end_col - start_col == 2 * dc or end_col - start_col == -2 * dc):
                if 0 <= mid_r < 5 and 0 <= mid_c < 5 and new_state[mid_r][mid_c] == 'D':
                    new_state[mid_r][mid_c] = '.'  # Capture the dog
    
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
    # Check if tiger has won (10 or more dogs captured)
    dog_count = sum(row.count('D') for row in current_state)
    if dog_count <= 6:
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
    initial_dogs = sum(row.count('D') for row in initial_state)
    current_dogs = sum(row.count('D') for row in current_state)
    return initial_dogs - current_dogs

# Modified minimax functions specifically for Tiger vs Dogs
def tiger_max_value(current_state, depth, alpha, beta):
    """Maximizing player's (Tiger) value function in Minimax with Alpha-Beta pruning."""
    global state_counter
    state_counter += 1

    if is_game_over(current_state) or depth == 0:
        return evaluate(current_state, MAX_PLAYER)

    max_eval = -float('inf')
    for move in get_valid_moves(current_state, 'T'):
        next_state = make_move(copy.deepcopy(current_state), move[0], move[1], MAX_PLAYER)
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
        return evaluate(current_state, MAX_PLAYER)  # Use evaluation function for dogs

    max_eval = -float('inf')
    for move in get_dog_possible_moves(current_state):
        next_state = make_move(copy.deepcopy(current_state), move[0], move[1], MAX_PLAYER)
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
        next_state = make_move(copy.deepcopy(current_state), move[0], move[1], MIN_PLAYER)
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
        next_state = make_move(copy.deepcopy(current_state), move[0], move[1], MIN_PLAYER)
        eval_score = dog_max_value(next_state, depth - 1, alpha, beta)
        min_eval = min(min_eval, eval_score)
        if min_eval <= alpha:  # Alpha cutoff
            return min_eval
        beta = min(beta, min_eval)
    return min_eval

def find_tiger_best_move(current_state):
    valid_moves = get_valid_moves(current_state, 'T')
    print("Valid moves:\n", valid_moves)  # Debugging line to check the moves list

    if valid_moves:
        best_move = valid_moves[0]  # Assuming you're selecting the first valid move
        
        # best_move is a tuple like ((2, 2), (1, 2)), so we need to unpack it correctly
        start_coords, end_coords = best_move  # Unpack the move correctly
        
        start_r, start_c = start_coords  # Extract row and column of start
        end_r, end_c = end_coords  # Extract row and column of end
        
        # Debugging output to verify
        print(f"Best move: {best_move}")
        print(f"Unpacked move: ({start_r}, {start_c}) -> ({end_r}, {end_c})")
        
        return (start_r, start_c, end_r, end_c)

    return None  # Return None if no valid moves are available
def find_dogs_best_move(current_state):
    valid_moves = get_dog_possible_moves(current_state)
    print("Valid moves for dogs:\n", valid_moves)  # Debugging line to check the moves list

    if valid_moves:
        best_move = valid_moves[0]  # Assuming you're selecting the first valid move
        
        # best_move is a tuple like ((2, 2), (3, 2)), so we need to unpack it correctly
        start_coords, end_coords = best_move  # Unpack the move correctly
        
        start_r, start_c = start_coords  # Extract row and column of start
        end_r, end_c = end_coords  # Extract row and column of end
        
        # Debugging output to verify
        print(f"Best move: {best_move}")
        print(f"Unpacked move: ({start_r}, {start_c}) -> ({end_r}, {end_c})")
        
        return (start_r, start_c, end_r, end_c)

    return None  # Return None if no valid moves are available

def Tiger_vs_Dogs_main():
    global state, state_counter, user_choice
    state_counter = 0
    game_board()  # Set up the initial board
    print_state()

    user_choice = ''
    while user_choice not in ['T', 'D']:
        user_choice = input("Do you want to play as the Tiger (T) or the Dogs (D)? ").strip().upper()
    
    user_player = user_choice
    ai_player = MIN_PLAYER if user_player == MAX_PLAYER else MAX_PLAYER
    current_player = MAX_PLAYER  # Tiger always starts first

    depth = 3 
    while True:
        try:
            depth = int(input("Enter the difficulty level (depth for minimax, higher means harder, e.g., 3): "))
            if depth > 0:
                print("Depth should be at least 1. Using default depth 3.")
                depth = 3
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
            else:
                print("No valid moves available for you!")
        else:
            # AI'S TURN
            print("AI is thinking...")
            start_time = time.time()
            move = find_best_move(state, depth, get_valid_moves, make_move, evaluate, ai_player, MAX_PLAYER, MIN_PLAYER, is_game_over)
            move_time = time.time() - start_time
            tiger_move_times.append(move_time)
            print(f"AI move took {move_time:.4f} seconds.")

            if move:
                (start_r, start_c), (end_r, end_c) = move
                state = make_move(state, (start_r, start_c), (end_r, end_c), current_player)
            else:
                print("AI has no valid moves!")

        print_state()

        # Switch player
        current_player = MIN_PLAYER if current_player == MAX_PLAYER else MAX_PLAYER

    # Game over
    winner = "Tiger" if evaluate(state, MAX_PLAYER) > 0 else "Dogs"
    print(f"Game Over! {winner} wins!")

def get_move_input():
    while True:
        user_input = input("Enter your move as 'start_row,start_col end_row,end_col': ")
        try:
            parts = user_input.strip().split()
            start = tuple(map(int, parts[0].split(',')))
            end = tuple(map(int, parts[1].split(',')))
            return (start, end)
        except (ValueError, IndexError):
            print("Invalid format. Please enter your move like: '1,2 1,3'")

if __name__ == "__main__":
    Tiger_vs_Dogs_main()

