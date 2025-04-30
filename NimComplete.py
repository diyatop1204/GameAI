from minimaxcomplete import *
import copy
import time
nim_move_times=[]

# 1. Game State Representation: list of integers
state = None
MAX_PLAYER = 'AI'
MIN_PLAYER = 'User'
EMPTY_CELL = '|'
state_counter = 0  # Initialise state counter

def initialize_state():
    """Initializes the game state (board) to empty."""
    global state
    num_rows = 4
    state = [2 * i + 1 for i in range(num_rows)]

def print_state():
    max_length = max(state) 
    print("\nCurrent Pyramid:")
    for i  in range(len(state)):
        row_value = state[i]
        space = (max_length - row_value) // 2
        print( str(i) + '' * space + '|' * row_value)

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
    #Checks that the remmoval of sticks is possible (i.e The row exists to take sticks out and that there are sticks left in the row)
    return 0 <= row < len(current_state) and 1 <= k <= current_state[row] 

#Peforms the move. It checks if the move is valid with terms of the game,  if it is a vlid move, it copies the current state of the game and removes the sticks from the row. The new state with the sticks taken out is then saved as the new state.
def make_move(current_state, row, k, player):
    """Makes a move on the state if it is valid."""
    if not is_valid_move(current_state, row, k): #Checks if the move is valid, if not it returns the normal 
        return current_state
    new_state = copy.deepcopy(current_state)

    # Remove the first k sticks from new_state[row]
    new_state[row] = new_state[row] - k
    return new_state


# 3. Winning Function - Checks which player has won at the terminal end of a game tree branch.

def winner(current_state, player):
    if all(row == 0 for row in current_state):
        # print(player)
        if (player == MAX_PLAYER):
            return -1 #Indicates MAX took last stick , meaning machine lost
        if (player == MIN_PLAYER): #Indicates MIN took last stick
            return +1
    return 0

def evaluate(current_state, player):

    if all(row == 0 for row in current_state):
        if player == MAX_PLAYER: #If current playyer is the AI when there are already no sticks left, AI wins
            return 1
        else:
            return -1

    #For when player is not in a terminal state: Based on solved theory of NIM, A xor(Nim Sum) of 0 means whoever the current player is in a losing position
    nim_sum = 0
    for row in current_state:
        nim_sum ^= row

    if nim_sum != 0:
        return 1
    else:
        return -1
    
def is_game_over(current_state, get_valid_moves, winner, player): #Checks if the game is over
    """Game is over when every row is empty."""
    return all(row == 0 for row in current_state)

def Nim_main():

    global state
    initialize_state()
    current_player = MAX_PLAYER  # MAX starts first

    print("Welcome to Nim vs Computer Complete Tree Search ")
   


    #Note: Get number of rows of sticks
    try:
        num_rows = int(input("Enter the number of rows of sticks "))
    except ValueError:
        print("Invalid input, defaulting to 4 rows.")
        num_rows = 4
    state = [2 * i + 1 for i in range(num_rows)]


 

    first_move_chooser = 1  # Default computer first
    while True:
        try:
            first_move_input = input("Who should make the first move? (1 - Computer, 2 - You ): ")
            first_move_chooser = int(first_move_input)
            if first_move_chooser not in [1, 2]:
                print("Invalid choice. Please enter 1 or 2. Computer will go first by default.")
                first_move_chooser = 1
            break
        except ValueError:
            print("Invalid input. Please enter 1 or 2. Computer will  go first by default.")
            first_move_chooser = 1
            break

    if first_move_chooser == 1:
        print("Computer  will make the first move.")
        current_player = MAX_PLAYER
    else:
        print("You will make the first move.")
        current_player = MIN_PLAYER

    while True:
        print_state()
        if current_player == MAX_PLAYER:
            print("Computer  is thinking...")
            nim_start_time = time.time() #start the timer for decision time
            best_move = find_best_move(state, get_valid_moves, make_move, MAX_PLAYER, MIN_PLAYER, is_game_over, winner, current_player) 
            nim_end_time = time.time() # end the timer
            state = make_move(state, best_move[0], best_move[1], MAX_PLAYER)
            current_player = MIN_PLAYER
            
            # Save move time
            nim_move_time = nim_end_time - nim_start_time
            nim_move_times.append(nim_move_time)
        else:
            print("Your turn")
            best_move_user = find_best_move_user(state, get_valid_moves, make_move,  MAX_PLAYER, MIN_PLAYER, is_game_over, winner, current_player)
            print("The best move for the user is: (row to remove, how many sticks to remove)", best_move_user)
            while True:
                try:
                    row_input = input("Enter row to remove stick (0 (Top) - Amount of Rows Seleced(Bottom))")
                    stick_input = input("How many sticks to remove? ")
                    row = int(row_input)
                    k = int(stick_input)
                    if is_valid_move(state, row, k):
                        break
                    else:
                        print("Invalid move. There are no sticks in this row Try again:")
                except ValueError:
                    print("Invalid format. Enter row to remove stick (0 (Top) - Amount of Rows Selected (Bottom)) and how many sticks to remove")

            state = make_move(state, row, k, MIN_PLAYER) #Remakes the state as chips have been removed
            
            current_player = MAX_PLAYER

        #When actual game is over, checks who was the last to take a stick out and won the game
        if is_game_over(state, get_valid_moves, evaluate, current_player):
            print_state()
            # The player who takes the last stick loses.
            if current_player == MAX_PLAYER:
                print("\nNo sticks left. You lose")
            else:
                print("\nNo sticks left. You win")
            break
        
        #Printing out the Move time summary
        if nim_move_times:
            nim_average_time = sum(nim_move_times) / len(nim_move_times)
            print("\n=== Scalability Test Result ===")
            print(f"Total moves made by computer: {len(nim_move_times)}")
            print(f"Average move time: {nim_average_time:.4f} seconds")
            print(f"Maximum move time: {max(nim_move_times):.4f} seconds")
            print(f"Minimum move time: {min(nim_move_times):.4f} seconds")