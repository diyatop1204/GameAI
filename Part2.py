import TicTacToe as ttt
import TicTacToeComplete as tttc
import Nim as Nim
import NimComplete as NimC
import TigerVsDogs as Td

# Basic Game Loop
if __name__ == "__main__":
    game = 1

    while True:
        try:
            game_input = input("Which Game would you like to play? TicTacToe = 1, Nim = 2, Tiger vs Dogs = 3 ")
            game = int(game_input)
            if game < 1:
                print("Invalid game selection - TicTacToe = 1, Nim = 2, Tiger vs Dogs = 3 ")
                game = 1
            break
        except ValueError:
            print("Invalid input. Please enter an integer game code option. Defaulting to Tic Tac Toe - 1.")
            game = 1
            break

    if game == 1:  
        print(f"Setting up Tic Tac Toe")
        while True:
            try:
                algorithim_input = input("Would you like to play with complete tree search = 1  or with Alpha Beta Pruning = 2? ")
                algorithim = int(algorithim_input)
                if algorithim == 1:
                    print(f"Starting TicTacToe with Complete Tree Search")
                    tttc.TicTacToe_main()
                    break
                elif algorithim == 2:                    
                    print(f"Starting TicTacToe with Alpha Beta Pruning")
                    ttt.TicTacToe_main()
                    break
                else:
                    print("Invalid Selection Defaulting to Alpha Beta Pruning algorithim")
                    ttt.TicTacToe_main()
                    break           
            except ValueError:
                print("Invalid input, Defaulting to Alpha Beta Pruning algorithim")
                algorithim = 1
                break

    if game == 2:  
        print(f"Setting up Nim")
        while True:
            try:
                algorithim_input = input("Would you like to play with complete tree search = 1  or with Alpha Beta Pruning = 2? ")
                algorithim = int(algorithim_input)
                if algorithim == 1:
                    print(f"Starting Nim with Complete Tree Search")
                    NimC.Nim_main()
                    break
                elif algorithim == 2:                    
                    print(f"Starting Nim with Alpha Beta Pruning")
                    Nim.Nim_main()
                    break
                else:
                    print("Invalid Selection Defaulting to Alpha Beta Pruning algorithim")
                    ttt.TicTacToe_main()
                    break           
            except ValueError:
                print("Invalid input, Defaulting to Alpha Beta Pruning algorithim")
                algorithim = 1
                break
 
    if game == 3: 
        print("Setting up Tiger vs Dogs")
        while True: 
            try:
                print("Starting Tiger vs Dogs with Alpha Beta Pruning")
                Td.Tiger_vs_Dogs_main()
                break
            except Exception as e:
                print(f"There was an error: {e}")
                break