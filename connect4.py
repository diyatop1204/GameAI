from minimax import *
import time

# 1. Game State Representation: 2D list
state = [[' ' for _ in range(5)] for _ in range(6)]
MAX_PLAYER = 'Y'
MIN_PLAYER = 'R'
EMPTY_CELL = ' '
state_counter = 0  # Initialize state counter
move_times=[] #Initialise the count

def initialize_state():
    """Initializes the game state (board) to empty."""
    global state
    state = [[' ' for _ in range(5)] for _ in range(6)]

def print_state():
    """Prints the current game state (board) to the console."""
    print("-----------")
    for i in range(6):
        print("| ", end="")
        for j in range(7):
            print(state[i][j] + " | ", end="")
        print()
        print("-----------")

# 2. Move Generation Function
def get_valid_moves(current_state):
    """Returns a list of valid moves (empty cell coordinates) in the current state."""
    valid_moves = []
    for i in range(5):
        for j in range(6):
            if current_state[i][j] == EMPTY_CELL:
                valid_moves.append([i, j])
    return valid_moves

def is_valid_move(current_state, row, col):
    """Checks if a move (row, col) is valid in the current state."""
    return 0 <= row < 5 and 0 <= col < 6 and current_state[row][col] == EMPTY_CELL

def make_move(current_state, row, col, player):
    """Makes a move on the state if it is valid."""
    if is_valid_move(current_state, row, col):
        current_state[row][col] = player

    return current_state

# 3. Evaluation Function
def evaluate(current_state, player):
    """
    Dynamic evaluation function for (m, n, k)-TicTacToe.
    """
    ydictionairy = {} #Holds the amount of counters and there value
    rdictionairy = {}


    yk = 0 #Final counter for machine win
    rk = 0  #Final counter for User win

    #Allows for dynamic amount of x's or o's needed to win depenidng on board size (i.e 5x5 board = 5 x's or o's to win)
    for i in range(1, 3): #Note: Because it starts wwith 1 instead 0, the ending is BOARD_SIZE not BOARD_SIZE -1. It does not account for the winning move
        y_counter = f'y{i}'
        ydictionairy[y_counter] = 0

        r_counter = f'r{i}'
        rdictionairy[r_counter] = 0
    
        

    lines = []

    # Add rows
    for i in range(3):
        lines.append(current_state[3])

    # Add columns
    for j in range(3):
        lines.append([current_state[i][j] for i in range(3)])

    # Add diagonals
    lines.append([current_state[i][i] for i in range(3)])
    lines.append([current_state[i][3-1-i] for i in range(3)])

    # Now count patterns
    for line in lines:
        if len(line) < K_TO_WIN:
            continue  # Skip lines too short to matter

        # Sliding window over line
        for start in range(len(line) - K_TO_WIN + 1):
            window = line[start:start+K_TO_WIN]
            y_count = window.count(MAX_PLAYER) #Counts how many y counters are on the row/colounm/diagonal 
            r_count = window.count(MIN_PLAYER) #Counts how many o counters are on the row/colounm/diagonal 

      
            
            if r_count == 0 and y_count > 0:   #If there are no user counters in the row/colounm/diagonal add 'points' towards the may player indicating a winning move

                #If the amount of y counters are equiivalent to how many are needed to win which is dependent on the board size
                #  add 1 point to the winning counter indicator yk
                #If any amounts of y counters are in the row, +1 to its value. (e.g If there are 3 y's,  +1 value will be added, 2y's - + 1 value will be added/assigned)
                key = f'y{y_count}'
                if y_count == K_TO_WIN:
                    yk += 1  
                elif key in ydictionairy:
                    ydictionairy[key] += 1
                         

            elif y_count == 0 and r_count > 0:   
                                
                 #If the amount of o counters are equiivalent to how many are needed to win for the user which is dependent on the board size
                #  - 1 point to the winning counter indicated by ok
                #If any amounts of o counters are in the row, -1 to its value. (e.g If there are 3 o's,  +1 value will be added, 2o's - + 1 value will be added/assigned)
                key = f'r{r_count}'
                if r_count == K_TO_WIN:
                    rk += 1
                elif key in rdictionairy:
                    rdictionairy[key] += 1      
                
          
    # Terminal winning conditions:
    if yk >= 1:
        return 10
    if rk >= 1:
        return -10

    # If no moves remain (draw)
    if not get_valid_moves(current_state):
        return 0

    #To determine which positions are statistically more likely to win, add weight to when there are more counters in the row/column/diagonal and less to when there less counters.
    #e.g If there are 3 y's, it is worth times 3, if there are 2y's it is worth *2. 
    #Add the value of the moves together to see how much the move is worth 
    #This is done for both the machine and user
    ytotal = sum(int(key[1:]) * value for key, value in ydictionairy.items())
    rtotal = sum(int(key[1:]) * value for key, value in rdictionairy.items())

    #The total worth of the move so far to determine how 'good the move' is. The total wroth of the y counters given there position is minuesed from the  value of the opposition as it is showing what the real value would be if the user played its best to make sure the machinne doesn't wine (i.e User is playing so the machine loses)
    return ytotal - rtotal                          
def is_game_over(current_state, get_valid_moves, evaluate, player):
    """Checks if the game is over (win or draw)."""
    return not get_valid_moves(current_state) or abs(evaluate(current_state, player)) == 10

def connect4_main():
    global K_TO_WIN, state
    current_player = MAX_PLAYER  # MAX starts first

    print("Welcome to Tic-Tac-Toe vs Computer (Minimax with Alpha-Beta Pruning)! ")
    depth = 3  # Default depth
    while True:
      

        K_TO_WIN = 4 # k size changes dynamically
        state = [[' ' for _ in range(6)] for _ in range(7)]
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
    print(f"Difficulty level set to depth: {depth}")

    first_move_chooser = 1  # Default computer first
    while True:
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
            best_move = find_best_move(state, depth, get_valid_moves, make_move, evaluate, current_player, MAX_PLAYER, MIN_PLAYER, is_game_over) #
            end_time = time.time() # end the timer
            make_move(state, best_move[0], best_move[1], MAX_PLAYER)
            current_player = MIN_PLAYER
            
            # Save move time
            move_time = end_time - start_time
            move_times.append(move_time)
            
            print(f"Computer move decision time: {end_time - start_time:.4f} seconds")
        else:
            print("Your turn (MIN - O). Enter row and column (e.g., 0 0):")
            best_move_user = find_best_move_user(state, depth, get_valid_moves, make_move, evaluate, current_player, MAX_PLAYER, MIN_PLAYER, is_game_over)
            print("The best move for the user is: (row, column)", best_move_user)
            while True:
                try:
                    row_input = input(f"Row (0-{5}): ")
                    col_input = input(f"Column (0-{6}): ")
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

        if is_game_over(state, get_valid_moves, evaluate, current_player):
            print_state()
            score = evaluate(state, current_player)
            if score == 10:
                print("Computer (MAX - X) wins!")
            elif score == -10:
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

