from minimax import *
import time

## 3, 2, 3, 4

# 6 rows and 7 columns
# 1. Game State Representation: 2D list
state = [[' ' for _ in range(7)] for _ in range(6)]
MAX_PLAYER = 'Y'
MIN_PLAYER = 'R'
EMPTY_CELL = ' '
state_counter = 0  # Initialize state counter
move_times=[] #Initialise the count

def initialize_state():
    """Initializes the game state (board) to empty."""
    global state
    state = [[' ' for _ in range(7)] for _ in range(6)]

def print_state():
    """Prints the current game state (board) to the console."""
    print("-----------------------------")
    for i in range(6):
        print("| ", end="")
        for j in range(7):
            print(state[i][j] + " | ", end="")
        print()
        print("-----------------------------")

# 2. Move Generation Function
def get_valid_moves(current_state):
    """Returns a list of valid moves (empty cell coordinates) in the current state."""
    valid_moves = []
    

    # getting the coordinate values through the indexes and gets the sublists from the board
   
    for i in range(6):  
        for j in range(7):
            # if current_state[i][j] == EMPTY_CELL:
            #     valid_moves.append([i, j])
            
            # Check the bottom row of the board to see if any cells are empty
            if (current_state[5][j] == EMPTY_CELL):
                valid_moves.append([5, j])

            
            elif i < 5 and  (current_state[i][j] == EMPTY_CELL and current_state[i + 1][j] != EMPTY_CELL):
                valid_moves.append([i, j])
    return valid_moves

def is_valid_move(current_state, row, col):
    """Checks if a move (row, col) is valid in the current state."""

    if col < 0 or col > 7:
        return False

    if row == -1:
        for current_row in range(len(current_state)-1, -1, -1):
            if current_state[current_row][col] == EMPTY_CELL:
                return True
        
        return False 
    else:
        if row == 5 and current_state[row][col] == EMPTY_CELL:
            return True

        elif row < 5 and  (0 <= row < 6 and 0 <= col < 7 and current_state[row][col] == EMPTY_CELL  and current_state[row + 1][col] != EMPTY_CELL):
            return True

        else:
            return False
    

def make_move(current_state, row, col, player):
    """Makes a move on the state if it is valid."""

    if is_valid_move(current_state, row, col):
        if row == -1:
            for current_row in range(len(current_state)-1, -1, -1):
                if current_state[current_row][col] == EMPTY_CELL:
                    current_state[current_row][col] = player
                    break
        else:
            # print(row, col)
            current_state[row][col] = player

    return current_state

# 3. Evaluation Function
def evaluate(current_state, player):

    ydictionairy = {} #Holds the amount of counters and there value
    rdictionairy = {}
    global r_count
    global y_count
    global yk
    yk = 0 #Final counter for machine win
    rk = 0  #Final counter for User win

    #Allows for dynamic amount of x's or o's needed to win depenidng on board size (i.e 7x7 board = 7 x's or o's to win)
    for i in range(1, 4): #Note: Because it starts wwith 1 instead 0, the ending is BOARD_SIZE not BOARD_SIZE -1. It does not account for the winning move
        y_counter = f'y{i}'
        ydictionairy[y_counter] = 0

        r_counter = f'r{i}'
        rdictionairy[r_counter] = 0
    
        

    lines = []

    # Add rows
    for i in range(6):
        lines.append(current_state[i])

    # Add columns
    for j in range(7):
        lines.append([current_state[i][j] for i in range(6)])

   

    # Diagonals: top-left to bottom-right
    # Valid starting positions: rows 0 to 6 - 4 and cols 0 to 7 - 4
    for row in range(6 - K_TO_WIN + 1):      # rows 0 to 2 
        for col in range(7 - K_TO_WIN + 1):  # columns 0 to 3 
            diag = [current_state[row + i][col + i] for i in range(K_TO_WIN)]
            lines.append(diag)

    # Diagonals: bottom-left to top-right
    # Valid starting positions: rows 3 to 5 and cols 0 to 7 - 4
    for row in range(K_TO_WIN - 1, 6):       # rows 3 to 5 inclusive
        for col in range(7 - K_TO_WIN + 1):    # cols 0 to 3 inclusive
            diag = [current_state[row - i][col + i] for i in range(K_TO_WIN)]
            lines.append(diag)


    # Now count patterns
    for line in lines:
        if len(line) < K_TO_WIN:
            continue  # Skip lines too short to matter

        # Sliding window over line
        for start in range(len(line) - K_TO_WIN + 1):
            window = line[start:start+K_TO_WIN]
            y_count = window.count(MAX_PLAYER) #Counts how many y counters are on the row/colounm/diagonal 
            r_count = window.count(MIN_PLAYER) #Counts how many o counters are on the row/colounm/diagonal 

      
            
            #If there are no user counters in the row/colounm/diagonal add 'points' towards the may player indicating a winning move

                #If the amount of y counters are equiivalent to how many are needed to win which is dependent on the board size
                #  add 1 point to the winning counter indicator yk
                #If any amounts of y counters are in the row, +1 to its value. (e.g If there are 3 y's,  +1 value will be added, 2y's - + 1 value will be added/assigned)
                
               
            
            if r_count == 0 and y_count > 0:   #If there are no user counters in the row/colounm/diagonal add 'points' towards the max player indicating a winning move

            #If the amount of x counters are equiivalent to how many are needed to win which is dependent on the board size
            #  add 1 point to the winning counter indicator xk
            #If any amounts of x counters are in the row, +1 to its value. (e.g If there are 3 x's,  +1 value will be added, 2x's - + 1 value will be added/assigned)
                
                if y_count < K_TO_WIN:
                    key = f'y{y_count}'
                if y_count == K_TO_WIN:
                    yk += 1  
                elif y_count < K_TO_WIN and key in ydictionairy:
                    ydictionairy[key] += 1  #Gives weight on value of move depending if it is 3 reds, 2reds, etc. Point is added only if it appears not if all appear
                    ydictionairy[key] *= y_count

            elif y_count == 0 and r_count > 0:    
                if r_count < K_TO_WIN:
                    key = f'r{r_count}'
                if r_count == K_TO_WIN:
                    rk += 1  
                elif r_count < K_TO_WIN and key in ydictionairy:
                    rdictionairy[key] += 1 
                    rdictionairy[key] *= r_count    
            
        
                            
                #If the amount of o counters are equiivalent to how many are needed to win for the user which is dependent on the board size
            #  - 1 point to the winning counter indicated by ok
            #If any amounts of o counters are in the row, -1 to its value. (e.g If there are 3 o's,  +1 value will be added, 2o's - + 1 value will be added/assigned)
            
            
  
                
          
    # Terminal winning conditions:
    if yk > 0:
        return 10
    if rk > 0:
        return -10

     # If no moves remain (draw)
    if not get_valid_moves(current_state):
        return 0
   

    #To determine which positions are statistically more likely to win, add weight to when there are more counters in the row/column/diagonal and less to when there less counters.
    #e.g If there are 3 y's, it is worth times 3, if there are 2y's it is worth *2. 
    #Add the value of the moves together to see how much the move is worth 
    #This is done for both the machine and user
    
    global ytotal
    global rtotal
   

    # ytotal = sum(int(key[1:]) * value for key, value in ydictionairy.items())
    # rtotal = sum(int(key[1:]) * value for key, value in rdictionairy.items())

    #The total worth of the move so far to determine how 'good the move' is. The total wroth of the y counters given there position is minuesed from the  value of the opposition as it is showing what the real value would be if the user played its best to make sure the machinne doesn't wine (i.e User is playing so the machine loses)
    ytotal = sum(ydictionairy.values())
    rtotal = sum(rdictionairy.values())
    return ytotal - rtotal  


                            
def is_game_over(current_state, get_valid_moves, evaluate, player):
    """Checks if the game is over (win or draw)."""
    return not get_valid_moves(current_state) or abs(evaluate(current_state, player)) == 10

def connect4_main():
    global K_TO_WIN, state
    current_player = MAX_PLAYER  # MAX starts first

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Welcome to Connect 4 vs Computer (Minimax with Alpha-Beta Pruning)! ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    depth = 3  # Default depth
    while True:
      

        K_TO_WIN = 4
        state = [[' ' for _ in range(7)] for _ in range(6)]
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
            first_move_input = input("Computer (Y): 1,\nYou (R): 2?\n Who should make the first move? (1 or 2): ")
            first_move_chooser = int(first_move_input)
            if first_move_chooser not in [1, 2]:
                print("Invalid choice. Please enter 1 or 2. Computer (Y) will go first by default.")
                first_move_chooser = 1
            break
        except ValueError:
            print("Invalid input. Please enter 1 or 2. Computer (X) will go first by default.")
            first_move_chooser = 1
            break

    if first_move_chooser == 1:
        print("Computer, Yellow (Y) will make the first move.")
        current_player = MAX_PLAYER
    else:
        print("You, Red (R) will make the first move.")
        current_player = MIN_PLAYER

    while True:
        print_state()
        if current_player == MAX_PLAYER:
            print("Computer (MAX - Y) is thinking...")
            start_time = time.time() #start the timer for decision
            best_move = find_best_move(state, depth, get_valid_moves, make_move, evaluate, current_player, MAX_PLAYER, MIN_PLAYER, is_game_over) #
            print(best_move)
            end_time = time.time() # end the timer
            make_move(state, best_move[0], best_move[1], MAX_PLAYER)
            current_player = MIN_PLAYER
            
            # Save move time
            move_time = end_time - start_time
            move_times.append(move_time)
            
            print(f"Computer move decision time: {end_time - start_time:.4f} seconds")
        else:
            print("Your turn (MIN  - R). Enter column (0-6): ")
            best_move_user = find_best_move_user(state, depth, get_valid_moves, make_move, evaluate, current_player, MAX_PLAYER, MIN_PLAYER, is_game_over)
            print("The best move for the user is column", best_move_user[-1])
            while True:
                try:
                    col = int(input(f"Column (0-6): "))
                    if is_valid_move(state, -1, col):
                        break
                    else:
                        print("Invalid move. Cell is not empty or out of bounds. Try again")
                except ValueError:
                    print("Invalid input format. Enter row and column as numbers (e.g., 0 0). Try again")
                    

            make_move(state, -1, col, MIN_PLAYER)
            current_player = MAX_PLAYER

        if is_game_over(state, get_valid_moves, evaluate, current_player):
            print_state()
            score = evaluate(state, current_player)
            if score == 10:
                print("\nComputer (MAX - Y) wins!\n")
                print(yk)
                print(ytotal)
                print(rtotal)
                
            elif score == -10:
                print("\nYou (MIN - R) win!\n")
            else:
                print("\nIt's a draw!\n")
            break
        if move_times:
            average_time = sum(move_times) / len(move_times)
            print("\n=== Scalability Test Result ===")
            print(f"Total moves made by computer: {len(move_times)}")
            print(f"Average move time: {average_time:.4f} seconds")
            print(f"Maximum move time: {max(move_times):.4f} seconds")
            print(f"Minimum move time: {min(move_times):.4f} seconds")

