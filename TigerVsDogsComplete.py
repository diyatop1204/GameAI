import copy
from functools import partial
import time

MAX_PLAYER = 'T'  # Tiger
MIN_PLAYER = 'D'  # Dogs
state_counter = 0

# Initialize the board
def game_board():
    """Initialize the game board with tigers and dogs in starting positions"""
    return [
        ['D', 'D', 'D', 'D', 'D'],
        ['D', '.', '.', '.', 'D'],
        ['D', '.', 'T', '.', 'D'],
        ['D', '.', '.', '.', 'D'],
        ['D', 'D', 'D', 'D', 'D']
    ]

# Print the board
def print_state(current_state):
    """Print the current state of the board"""
    print("\n  0 1 2 3 4")
    for i, row in enumerate(current_state):
        print(f"{i} {' '.join(row)}")

# Evaluate the state from MAX_PLAYER's perspective
def evaluate(state):
    """Evaluates the board state from the tiger's perspective"""
    tiger_pos = find_tiger(state)
    
    # Count dogs
    dog_count = sum(row.count('D') for row in state)
    
    # If 6 or more dogs have been captured, tiger wins
    if dog_count <= 10:  # Original dog count is 16, so 16 - 6 = 10
        return 1000
    
    # If tiger doesn't exist or is trapped, dogs win
    if not tiger_pos:
        return -1000
    
    # Get valid moves for tiger
    tiger_moves = []
    r, c = tiger_pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 5 and 0 <= nc < 5 and state[nr][nc] == '.':
            tiger_moves.append((nr, nc))
    
    if not tiger_moves:  # Tiger is trapped
        return -1000
    
    # Otherwise, score based on number of dogs and tiger's mobility
    return (16 - dog_count) * 100 + len(tiger_moves) * 10

# Check if the state is terminal
def is_terminal(state):
    """Check if the game is over (tiger captured or trapped, or 6+ dogs captured)"""
    # Check if 6 or more dogs have been captured
    dog_count = sum(row.count('D') for row in state)
    if dog_count <= 10:  # 16 - 6 = 10 dogs remaining means 6 are captured
        return True

    # Check if tiger has been captured
    tiger_pos = find_tiger(state)
    if not tiger_pos:
        return True
    
    # Check if tiger is trapped (no valid moves)
    moves = get_all_moves(state, MAX_PLAYER)
    if not moves:
        return True
    
    # Check if dogs have no valid moves
    dog_moves = get_all_moves(state, MIN_PLAYER)
    if not dog_moves:
        return True
    
    return False

# Generate all valid moves for a player
def get_all_moves(state, player):
    """Generate all valid moves for the specified player (Tiger 'T' or Dogs 'D')"""
    moves = []
    
    if player == MAX_PLAYER:  # Tiger's turn
        tiger_pos = find_tiger(state)
        if tiger_pos:
            r, c = tiger_pos
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                          (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 5 and 0 <= nc < 5 and state[nr][nc] == '.':
                    moves.append(((r, c), (nr, nc)))
    
    elif player == MIN_PLAYER:  # Dogs' turn
        dog_positions = find_dogs(state)
        for r, c in dog_positions:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 5 and 0 <= nc < 5 and state[nr][nc] == '.':
                    moves.append(((r, c), (nr, nc)))
    
    return moves

# Apply a move to the state and return the new state
def apply_move(state, move):
    """Apply a move to the board and return the new state"""
    new_state = copy.deepcopy(state)
    (i, j), (ni, nj) = move
    player = new_state[i][j]  # Get the player making the move
    
    # Execute the move
    new_state[ni][nj] = player
    new_state[i][j] = '.'
    
    # If Tiger is moving, check for dogs to remove
    if player == MAX_PLAYER:
        remove_adjacent_dogs_if_surrounded(new_state, ni, nj)
    
    return new_state

# Complete tree search minimax algorithm 
def minimax(state, maximizing_player):
    """Minimax algorithm with complete tree search"""
    global state_counter
    state_counter += 1
    
    if is_terminal(state):
        return evaluate(state), None
    
    player = MAX_PLAYER if maximizing_player else MIN_PLAYER
    moves = get_all_moves(state, player)
    
    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            eval, _ = minimax(apply_move(state, move), False) #_ used to ignore one of the return values
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            eval, _ = minimax(apply_move(state, move), True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move

# Get move from user
def get_user_move(state, player):
    """Get a valid move from the user"""
    valid_moves = get_all_moves(state, player)
    
    if not valid_moves:
        print(f"No valid moves for {player}!")
        return None
    
    print(f"Available {player} moves:")
    for i, move in enumerate(valid_moves):
        print(f"{i+1}: {player} at ({move[0][0]},{move[0][1]}) to ({move[1][0]},{move[1][1]})")
    
    while True:
        try:
            choice = int(input(f"\nEnter the number of your chosen move (1-{len(valid_moves)}): "))
            if 1 <= choice <= len(valid_moves):
                return valid_moves[choice - 1]
            else:
                print("Invalid choice. Please enter a number between 1 and", len(valid_moves))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Helper functions for tiger and dogs
def find_tiger(state):
    """Find the tiger's position on the board"""
    for r in range(5):
        for c in range(5):
            if state[r][c] == 'T':
                return (r, c)
    return None

def find_dogs(state):
    """Find all dog positions on the board"""
    dog_positions = []
    for r in range(5):
        for c in range(5):
            if state[r][c] == 'D':
                dog_positions.append((r, c))
    return dog_positions

def remove_adjacent_dogs_if_surrounded(new_state, end_row, end_col):
    """Remove adjacent dogs in a straight line if they are the only two dogs in that direction"""
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

# Main function
def Tiger_vs_Dogs_Complete_main():
    """Main function to run the Tiger vs Dogs game with complete minimax search"""
    global state_counter
    
    state = game_board()
    print_state(state)

    user_choice = ''
    while user_choice not in ['T', 'D']:
        user_choice = input("Do you want to play as the Tiger (T) or the Dogs (D)? ").strip().upper()

    user_player = user_choice
    ai_player = 'D' if user_player == 'T' else 'T'
    current_player = 'T'  # Tiger starts first

    while not is_terminal(state):
        print(f"\nIt's {current_player}'s turn.")
        if current_player == user_player:
            user_move = get_user_move(state, user_player)
            if user_move:
                state = apply_move(state, user_move)
            else:
                print("No valid moves available. Game over!")
                break
        else:
            print("AI is thinking...")
            state_counter = 0
            start_time = time.time()
            
            # Run complete tree search 
            try:
                _, ai_move = minimax(state, ai_player == MAX_PLAYER)
                
                move_time = time.time() - start_time
                print(f"AI move took {move_time:.4f} seconds.")
                print(f"States searched: {state_counter}")
                
                if ai_move:
                    print(f"AI chooses move: {ai_move}")
                    state = apply_move(state, ai_move)
                else:
                    print("AI has no valid moves. Skipping turn.")
            except RecursionError:
                moves = get_all_moves(state, ai_player)
                if moves:
                    import random
                    ai_move = random.choice(moves)
                    print(f"AI chooses move: {ai_move}")
                    state = apply_move(state, ai_move)
                else:
                    print("AI has no valid moves. Skipping turn.")

        print_state(state)
        current_player = 'D' if current_player == 'T' else 'T'

    print("\nGame Over.")
    
    # Determine winner
    tiger_pos = find_tiger(state)
    dog_count = sum(row.count('D') for row in state)
    
    if dog_count <= 10:
        print("Tiger wins by capturing enough dogs!")
    elif not tiger_pos:
        print("Dogs win by capturing the tiger!")
    elif not get_all_moves(state, 'T'):
        print("Dogs win by trapping the tiger!")
    else:
        print("Dogs have no valid moves. Tiger wins!")

if __name__ == "__main__":
    Tiger_vs_Dogs_Complete_main()