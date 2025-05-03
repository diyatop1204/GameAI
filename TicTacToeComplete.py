from minimaxcomplete import *
import time
global BOARD_SIZE
move_times=[] #Initialise the count
BOARD_SIZE = None
K_TO_WIN = None


# 1. Game State Representation: 2D list
state = [[' ' for _ in range(3)] for _ in range(3)]
MAX_PLAYER = 'X' #First starting player 
MIN_PLAYER = 'O' #Second player
EMPTY_CELL = ' '
state_counter = 0  # Initialize state counter

    

def print_state():
    """Prints the current game state (board) to the console."""
    print("----"*BOARD_SIZE)
    for i in range(BOARD_SIZE):
        print("| ", end="")
        for j in range(BOARD_SIZE):
            print(state[i][j] + " | ", end="")
        print()
        print("----"*BOARD_SIZE)

# 2. Move Generation Function
def get_valid_moves(current_state):
    """Returns a list of valid moves (empty cell coordinates) in the current state."""
    valid_moves = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if current_state[i][j] == EMPTY_CELL:
                valid_moves.append([i, j])
    return valid_moves

def is_valid_move(current_state, row, col):
    """Checks if a move (row, col) is valid in the current state."""
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and current_state[row][col] == EMPTY_CELL

def make_move(current_state, row, col, player):
    """Makes a move on the state if it is valid."""
    if is_valid_move(current_state, row, col):
        current_state[row][col] = player

    return current_state



#Checks for a winner
def winner(current_state, player):

    #Note checks if all the cells in column  match with the player symbol if it does, play wins
    for i in range(BOARD_SIZE):
       if all (current_state[k][i] == MAX_PLAYER for k in range(BOARD_SIZE)):
               return +1
       if all (current_state[k][i] == MIN_PLAYER for k in range(BOARD_SIZE)):
               return -1
           
          

    #Checks if all the cells in row matchs the player symbol
    for i in range(BOARD_SIZE):
       if all (current_state[i][k] == MAX_PLAYER for k in range(BOARD_SIZE)):
               return +1
       if all (current_state[i][k] == MIN_PLAYER for k in range(BOARD_SIZE)):
               return -1


    #Checks diagonal to see if it matches play symbol, showing a win  (i.e 0,0 1,1 2,2) 
    if all (current_state[k][k] == MAX_PLAYER for k in range(BOARD_SIZE)):
               return +1
    if all (current_state[k][k] == MIN_PLAYER for k in range(BOARD_SIZE)):
               return -1
 

    #Check Diagonal on the otherside to see if it matches player symbol, showing a win  (i.e 0,2 1,1, 2,0) 
    if all (current_state[k][BOARD_SIZE-1-k] == MAX_PLAYER for k in range(BOARD_SIZE)):
               return +1
    if all (current_state[k][BOARD_SIZE-1-k] == MIN_PLAYER for k in range(BOARD_SIZE)):
               return -1

    #If no winning conditions are met, there is a tie
    return 0    
       

def is_game_over(current_state, get_valid_moves, winner, player):
    """Checks if the game is over (win or draw)."""
    return not get_valid_moves(current_state) or abs(winner(current_state, player)) == 1 #Checks that either Max or Min has won by value being either 1 or -1, or checking get valid moves to see if there is a ties

def TicTacToe_main():
    global BOARD_SIZE, K_TO_WIN, state
    current_player = MAX_PLAYER  # MAX starts first
    print("Welcome to Tic-Tac-Toe vs Computer Complete Tree Search! ")
    while True:
        try:
            board_size_input = input("Enter board size (e.g., 3 for 3x3): ")
            BOARD_SIZE = int(board_size_input)
            if BOARD_SIZE < 3:
                print("Board size must be at least 3. Defaulting to 3.")
                BOARD_SIZE = 3
        except ValueError:
            print("Invalid input. Defaulting to board size 3.")
            BOARD_SIZE = 3
        
        K_TO_WIN = BOARD_SIZE # k size changes dynamically
        state = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        first_move_chooser = 1  # Default computer first
    
        try:
            first_move_input = input("Who should make the first move? (1 - Computer (X), 2 - You (O)): ")
            first_move_chooser = int(first_move_input)
            if first_move_chooser not in [1, 2]:
                print("Invalid choice. Please enter 1 or 2. Computer (X) will go first by default.")
                first_move_chooser = 1
            break
        except ValueError:
            print("Invalid input. Please enter 1 or 2. Computer (X) will go first by default.")
            first_move_chooser = 1
            break

    if first_move_chooser == 1:
        print("Computer (X) will make the first move.")
        current_player = MAX_PLAYER
    else:
        print("You (O) will make the first move.")
        current_player = MIN_PLAYER

    while True:
        print_state()
        if current_player == MAX_PLAYER:
            print("Computer (MAX - X) is thinking...")
            start_time = time.time() #start the timer for decision
            best_move = find_best_move(state,  get_valid_moves, make_move,  MAX_PLAYER, MIN_PLAYER, is_game_over, winner, current_player) 
            end_time = time.time() # end the timer
            make_move(state, best_move[0], best_move[1], MAX_PLAYER)
            current_player = MIN_PLAYER
            
            # Save move time
            move_time = end_time - start_time
            move_times.append(move_time)
            
            print(f"Computer move decision time: {end_time - start_time:.4f} seconds")
        else:
            print("Your turn (MIN - O). Enter row and column (e.g., 0 0):")
            best_move_user = find_best_move_user(state, get_valid_moves, make_move,  MAX_PLAYER, MIN_PLAYER, is_game_over, winner, current_player)
            print("The best move for the user is: (row, column)", best_move_user)
            while True:
                try:
                    row_input = input(f"Row (0-{BOARD_SIZE - 1}): ",)
                    col_input = input(f"Column (0-{BOARD_SIZE - 1}): ")
                    row = int(row_input)
                    col = int(col_input)
                    if is_valid_move(state, row, col):
                        break
                    else:
                        print("Invalid move. Cell is not empty or out of bounds. Try again:")
                except ValueError:
                    print("Invalid input format. Enter row and column as numbers (e.g., 0 0). Try again:")

            make_move(state, row, col, MIN_PLAYER)
            current_player = MAX_PLAYER
            
        if is_game_over(state, get_valid_moves, winner, current_player): 
            print_state(), 
            if winner(state, current_player) == 1: #Checks if MAX  has won.
                print("Computer (MAX - X) wins!")
            elif winner(state, current_player) == -1: #Checks if Min has won.
                print("You (MIN - O) win!")
            else:
                print("It's a draw!")
            break
        if move_times:
            average_time = sum(move_times) / len(move_times)
            print("\n=== Scalability Test Result ===")
            print(f"Total moves made by computer: {len(move_times)}")
            print(f"Average move time: {average_time:.4f} seconds")
            print(f"Maximum move time: {max(move_times):.4f} seconds")
            print(f"Minimum move time: {min(move_times):.4f} seconds")

