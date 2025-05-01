from minimax import *

# 1. Game State Representation: 2D list
state = [[' ' for _ in range(6)] for _ in range(7)]
MAX_PLAYER = 'Y'
MIN_PLAYER = 'R'
EMPTY_CELL = ' '
state_counter = 0  # Initialize state counter

def initialize_state():
    """Initializes the game state (board) to empty."""
    global state
    state = [[' ' for _ in range(6)] for _ in range(7)]

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
    for i in range(6):
        for j in range(7):
            if current_state[i][j] == EMPTY_CELL:
                valid_moves.append([i, j])
    return valid_moves

def is_valid_move(current_state, row, col):
    """Checks if a move (row, col) is valid in the current state."""
    return 0 <= row < 6 and 0 <= col < 7 and current_state[row][col] == EMPTY_CELL

def make_move(current_state, row, col, player):
    """Makes a move on the state if it is valid."""
    if is_valid_move(current_state, row, col):
        current_state[row][col] = player

    return current_state

# 3. Evaluation Function
def evaluate(current_state, player):
    """Evaluates the current game state and returns a score."""
    # Check rows, columns, and diagonals for wins
        
    for i in range(3):
       if all (current_state[k][i] == player for k in range(3)):
           if(player == MAX_PLAYER):
               return 10
           if(player == MIN_PLAYER):
               return -10
    for i in range(3):
       if all (current_state[i][k] == player for k in range(3)):
           if(player == MAX_PLAYER):
               return 10
           if(player == MIN_PLAYER):
               return -10           
    if all (current_state[k][k] == player for k in range(3)):
           if(player == MAX_PLAYER):
               return 10
           if(player == MIN_PLAYER):
               return -10 
    if all (current_state[k][2-k] == player for k in range(3)):
         if(player == MAX_PLAYER):
               return 10
         if(player == MIN_PLAYER):
               return -10  
    return 0  # No winner yet or draw (handled in is_game_over)                           
def is_game_over(current_state, get_valid_moves, evaluate, player):
    """Checks if the game is over (win or draw)."""
    return not get_valid_moves(current_state) or abs(evaluate(current_state, player)) == 10

def TicTacToe_main():
    initialize_state()
    current_player = MAX_PLAYER  # MAX starts first

    print("Welcome to Tic-Tac-Toe vs Computer (Minimax with Alpha-Beta Pruning)! ")
    depth = 3  # Default depth
    while True:
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
            best_move = find_best_move(state, depth, get_valid_moves, make_move, evaluate, current_player, MAX_PLAYER, MIN_PLAYER, is_game_over) #
            make_move(state, best_move[0], best_move[1], MAX_PLAYER)
            current_player = MIN_PLAYER
        else:
            print("Your turn (MIN - O). Enter row and column (e.g., 0 0):")
            while True:
                try:
                    row_input = input("Row (0-2): ")
                    col_input = input("Column (0-2): ")
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