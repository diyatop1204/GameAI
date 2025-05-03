from minimax import *
import copy
import time
nim_move_times=[]

# 1. Game State Representation: list of integers
state = None
MAX_PLAYER = 'AI'
MIN_PLAYER = 'User'
state_counter = 0  # Initialise state counter

def initialize_state():
    """Initializes the game state (board) to empty."""
    global state
    num_rows = 4
    state = []

def print_state():
    max_length = max(state) 
    print("\nCurrent Pyramid:")
    for i in range(len(state)):
        row = state[i] #Equivalent of number of rows
        space = (max_length - row) // 2
        print( str(i) + ' ' * space + '|' * row)

# 2. Move Generation Function
def get_valid_moves(current_state):
    """Returns a list of valid moves  in the current state."""
    valid_moves = []
       # Iterate over each row 
    for i in range(len(current_state)):
        # If the row is not empty, then generate moves
        sticks =  current_state[i] #Note: Checking if there are still sticks in the row
        if sticks > 0:
            # k is the number of sticks to remove (from 1 up to the full row length)
            for k in range(1, sticks + 1):
                valid_moves.append((i, k))
    return valid_moves

def is_valid_move(current_state, row, k):
    """Checks if a move  is valid in the current state."""
    return 0 <= row < len(current_state) and 1 <= k <= current_state[row]

def make_move(current_state, row, k, player):
    """Makes a move on the state if it is valid."""
    if not is_valid_move(current_state, row, k):
        return current_state
    new_state = copy.deepcopy(current_state)

    # Remove the first k chips from new_state[row]
    new_state[row] = new_state[row] - k
    return new_state
 

# 3. Evaluation Function
def evaluate(current_state, player):


    if all(row == 0 for row in current_state):
        if player == MAX_PLAYER: #If current playyer is the AI when there are already no sticks left, AI wins
            return 1
        else:
            return -1

    #For when player is not in a terminal state: Based on solved theory of NIM, A xor of 0 means whoever the current player is in a losing position
    nim_sum = 0
    for row in current_state:
        nim_sum ^= row

    if nim_sum != 0: #If after xor opperation, nim_sum is not zero,
        return 1
    else:
        return -1

        
def is_game_over(current_state, get_valid_moves, evaluate, player):
    """Game is over when every row is empty."""
    return all(row == 0 for row in current_state)

def Nim_main():

    global state
    initialize_state()
    num_sticks = 0
    current_player = MAX_PLAYER  # MAX starts first

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Welcome to Nim vs Computer (Minimax with Alpha-Beta Pruning)!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    depth = 3  # Default depth

    #Note: Get number of rows of sticks
    try:
        num_rows = int(input("Enter the number of rows (of sticks): "))

    except ValueError:
        print("Invalid input, defaulting to 4 rows.")
        num_rows = 4

    print()
    #Note: Get number of sticks in a row
    for i in range(num_rows):
        try:
            num_sticks = int(input(f"Enter the number of sticks in Row {i}: "))
            state.append(num_sticks)

        except ValueError:
            print("Invalid input, defaulting to increments of 2 in each row.")
            num_rows = 4
            state = [2 * i + 1 for i in range(num_rows)]    



    while True:
        try:
            depth_input = int(input("\nEnter the difficulty level (depth for minimax, higher means harder, e.g., 3): "))
            depth = depth_input
            if depth < 1:
                print("Depth should be at least 1. Using default depth 3.")
                depth = 3
            break
        except ValueError:
            print("Invalid input. Please enter an integer depth. Using default depth 3.")
            depth = 3
            break
    print(f"Difficulty level set to depth: {depth}")

    first_move_chooser = 1  # Default computer first
    while True:
        try:
            first_move_input = input("\nComputer : 1,\nYou: 2?\n Who should make the first move? (1 or 2): ")
            first_move_chooser = int(first_move_input)
            if first_move_chooser not in [1, 2]:
                print("Invalid choice. Please enter 1 or 2. Computer will go first by default.")
                first_move_chooser = 1
            break
        except ValueError:
            print("Invalid input. Please enter 1 or 2. Computer will go first by default.")
            first_move_chooser = 1
            break

    if first_move_chooser == 1:
        print("\nComputer will make the first move.")
        current_player = MAX_PLAYER
    else:
        print("\nYou will make the first move.")
        current_player = MIN_PLAYER

    while True:
        print_state()
        if current_player == MAX_PLAYER:
            print("\nComputer is thinking...")
            nim_start_time = time.time() #start the timer for decision time
            best_move = find_best_move(state, depth, get_valid_moves, make_move, evaluate, current_player, MAX_PLAYER, MIN_PLAYER, is_game_over) 
            nim_end_time = time.time() # end the timer
            state = make_move(state, best_move[0], best_move[1], MAX_PLAYER)
            current_player = MIN_PLAYER
            
            # Save move time
            nim_move_time = nim_end_time - nim_start_time
            nim_move_times.append(nim_move_time)
        else:
            print("\nYour turn!")
            while True:
                try:
                    row_input = input(f"\nEnter row to remove stick (Row 0 (Top) - Row {num_rows-1} (Bottom)): ")
                    stick_input = input("How many sticks to remove? ")
                    row = int(row_input)
                    k = int(stick_input)
                    if is_valid_move(state, row, k):
                        break
                    else:
                        print("Invalid move. There are no sticks in this row. Try again")
                except ValueError:
                    print(f"Invalid format. Enter row to remove stick (Row 0 (Top) - Row {num_rows-1} Selected (Bottom)) and how many sticks to remove")

            state = make_move(state, row, k, MIN_PLAYER) #Remakes the state as chips have been removed
            
            current_player = MAX_PLAYER

        if is_game_over(state, get_valid_moves, evaluate, current_player):
            print_state()
            # The player who takes the last stick loses.
            if current_player == MAX_PLAYER:
                print("\nNo sticks left. You lose :(\n")
            else:
                print("\nNo sticks left. You win!\n")
            break
        #Printing out the Move time summary
        if nim_move_times:
            nim_average_time = sum(nim_move_times) / len(nim_move_times)
            print("\n=== Scalability Test Result ===")
            print(f"Total moves made by computer: {len(nim_move_times)}")
            print(f"Average move time: {nim_average_time:.4f} seconds")
            print(f"Maximum move time: {max(nim_move_times):.4f} seconds")
            print(f"Minimum move time: {min(nim_move_times):.4f} seconds")