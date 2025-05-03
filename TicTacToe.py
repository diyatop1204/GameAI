from minimax import *
import time
global BOARD_SIZE


move_times=[] #Initialise the count
BOARD_SIZE = None
K_TO_WIN = None
# 1. Game State Representation: 2D list
state = []
MAX_PLAYER = 'X'
MIN_PLAYER = 'O'
EMPTY_CELL = ' '
state_counter = 0  # Initialize state counter

def print_state():
    """Prints the current game state (board) to the console."""
    separator = ("----" * BOARD_SIZE) + "-"
    print(separator)
    for i in range(BOARD_SIZE):
        print("|", end=" ")
        for j in range(BOARD_SIZE):
            print(state[i][j], end=" | ")
        print()  # Newline after row
        print(separator)


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

def evaluate(current_state, player):
    """
    Dynamic evaluation function for (m, n, k)-TicTacToe.
    """
    Xdictionairy = {} #Holds the amount of counters and there value
    odictionairy = {}


    xk = 0 #Final counter for machine win
    ok = 0  #Final counter for User win

    #Allows for dynamic amount of x's or o's needed to win depenidng on board size (i.e 5x5 board = 5 x's or o's to win)
    for i in range(1, BOARD_SIZE): #Note: Because it starts wwith 1 instead 0, the ending is BOARD_SIZE not BOARD_SIZE -1. It does not account for the winning move
        x_counter = f'x{i}'
        Xdictionairy[x_counter] = 0

        o_counter = f'o{i}'
        odictionairy[o_counter] = 0
    
        

    lines = []

    # Add rows
    for i in range(BOARD_SIZE):
        lines.append(current_state[i])

    # Add columns
    for j in range(BOARD_SIZE):
        lines.append([current_state[i][j] for i in range(BOARD_SIZE)])

    # Add diagonals
    lines.append([current_state[i][i] for i in range(BOARD_SIZE)])
    lines.append([current_state[i][BOARD_SIZE-1-i] for i in range(BOARD_SIZE)])

    # Now count patterns
    for line in lines:
        if len(line) < K_TO_WIN:
            continue  # Skip lines too short to matter

        # Sliding window over line
        for start in range(len(line) - K_TO_WIN + 1):
            window = line[start:start+K_TO_WIN]
            x_count = window.count(MAX_PLAYER) #Counts how many x counters are on the row/colounm/diagonal 
            o_count = window.count(MIN_PLAYER) #Counts how many o counters are on the row/colounm/diagonal 

      
            
            if o_count == 0 and x_count > 0:   #If there are no user counters in the row/colounm/diagonal add 'points' towards the max player indicating a winning move

                #If the amount of x counters are equiivalent to how many are needed to win which is dependent on the board size
                #  add 1 point to the winning counter indicator xk
                #If any amounts of x counters are in the row, +1 to its value. (e.g If there are 3 x's,  +1 value will be added, 2x's - + 1 value will be added/assigned)
                key = f'x{x_count}'
                if x_count == K_TO_WIN:
                    xk += 1  
                elif key in Xdictionairy:
                    Xdictionairy[key] += 1
                         

            elif x_count == 0 and o_count > 0:   
                                
                 #If the amount of o counters are equiivalent to how many are needed to win for the user which is dependent on the board size
                #  - 1 point to the winning counter indicated by ok
                #If any amounts of o counters are in the row, -1 to its value. (e.g If there are 3 o's,  +1 value will be added, 2o's - + 1 value will be added/assigned)
                key = f'o{o_count}'
                if o_count == K_TO_WIN:
                    ok += 1
                elif key in odictionairy:
                    odictionairy[key] += 1      
                
          
    # Terminal winning conditions:
    if xk >= 1:
        return 10
    if ok >= 1:
        return -10

    # If no moves remain (draw)
    if not get_valid_moves(current_state):
        return 0

    #To determine which positions are statistically more likely to win, add weight to when there are more counters in the row/column/diagonal and less to when there less counters.
    #e.g If there are 3 x's, it is worth times 3, if there are 2x's it is worth *2. 
    #Add the value of the moves together to see how much the move is worth 
    #This is done for both the machine and user
    xtotal = sum(int(key[1:]) * value for key, value in Xdictionairy.items())
    ototal = sum(int(key[1:]) * value for key, value in odictionairy.items())

    #The total worth of the move so far to determine how 'good the move' is. The total wroth of the x counters given there position is minuesed from the  value of the opposition as it is showing what the real value would be if the user played its best to make sure the machinne doesn't wine (i.e User is playing so the machine loses)
    return xtotal - ototal

        
                        
def is_game_over(current_state, get_valid_moves, evaluate, player):
    """Checks if the game is over (win or draw)."""
    return not get_valid_moves(current_state) or abs(evaluate(current_state, player)) == 10

def TicTacToe_main():
    global BOARD_SIZE, K_TO_WIN, state
    current_player = MAX_PLAYER  # MAX starts first

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Welcome to Tic-Tac-Toe vs Computer (Minimax with Alpha-Beta Pruning)!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    depth = 3  # Default depth
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
        try:
            depth_input = input("Enter the difficulty level (depth for minimax, higher means harder, e.g., 3): ")
            depth = int(depth_input)
            if depth < 1:
                print("Depth should be at least 1. Using default depth 3.")
                depth = 3
            break
        except ValueError:
            print("Invalid input. Please enter an integer depth. Using default depth 3.")
            depth = 3
            break
    print(f"Difficulty level set to depth: {depth}\n")

    first_move_chooser = 1  # Default computer first
    while True:
        try:
            first_move_input = input("Computer (X): 1,\nYou(O): 2?\n Who should make the first move? (1 or 2): ")
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
            best_move = find_best_move(state, depth, get_valid_moves, make_move, evaluate, current_player, MAX_PLAYER, MIN_PLAYER, is_game_over) 
            end_time = time.time() # end the timer
            make_move(state, best_move[0], best_move[1], MAX_PLAYER)
            current_player = MIN_PLAYER
            
            # Save move time
            move_time = end_time - start_time
            move_times.append(move_time)
            
            print(f"Computer move decision time: {end_time - start_time:.4f} seconds")
        else:
            print("Your turn (MIN - O). Enter row and column below (e.g., Row 0, Column 0)")
            best_move_user = find_best_move_user(state, depth, get_valid_moves, make_move, evaluate, current_player, MAX_PLAYER, MIN_PLAYER, is_game_over)
            print("The best move for the user is: (row, column)", best_move_user)
            while True:
                try:
                    row_input = input(f"\nRow (0-{BOARD_SIZE - 1}): ")
                    col_input = input(f"Column (0-{BOARD_SIZE - 1}): ")
                    row = int(row_input)
                    col = int(col_input)
                    if is_valid_move(state, row, col):
                        break
                    else:
                        print("Invalid move. Cell is not empty or out of bounds. Try again")
                except ValueError:
                    print("Invalid input format. Enter row and column as numbers (e.g., 0 0). Try again")

            make_move(state, row, col, MIN_PLAYER)
            current_player = MAX_PLAYER

        if is_game_over(state, get_valid_moves, evaluate, current_player):
            print_state()
            score = evaluate(state, current_player)
            if score == 10:
                print("\nComputer (MAX - X) wins!\n")
            elif score == -10:
                print("\nYou (MIN - O) win!\n")
            else:
                print("\nIt's a draw!\n")
            break
        if move_times:
            average_time = sum(move_times) / len(move_times)
            print("\n=== Scalability Test Result ===")
            print(f"Total moves made by computer: {len(move_times)}")
            print(f"Average move time: {average_time:.4f} seconds")
            print(f"Maximum move time: {max(move_times):.4f} seconds")
            print(f"Minimum move time: {min(move_times):.4f} seconds\n")

