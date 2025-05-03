import TicTacToe as ttt
import TicTacToeComplete as tttc
import Nim as Nim
import NimComplete as NimC
import TigerVsDogs as Td
import connect4 as c4

# Basic Game Loop
if __name__ == "__main__":
    game = 1

    while True:
        try:
            game = int(input("\nWhich Game would you like to play?\n TicTacToe: 1,\n Nim: 2,\n Tiger vs Dogs: 3,\n Connect 4: 4?\n\nEnter Game Number (i.e 1):  "))
            if game < 1:
                print("\nInvalid game selection - TicTacToe: 1, Nim: 2, Tiger vs Dogs: 3, Connect 4: 4")
                game = 1
            break
        except ValueError:
            print("Invalid input. Please enter an integer game code option. Defaulting to Tic Tac Toe.")
            game = 1
            break

    if game == 1:  
        print(f"Setting up Tic Tac Toe\n")
        while True:
            try:
                algorithm = int(input("Would you like to play with: \n Complete Tree Search: 1 or \n Alpha Beta Pruning = 2?\n\nEnter Algorithm Number: "))
                if algorithm == 1:
                    print("Starting TicTacToe with Complete Tree Search...\n")
                    tttc.TicTacToe_main()
                    break
                elif algorithm == 2:                    
                    print("Starting TicTacToe with Alpha Beta Pruning...\n")
                    ttt.TicTacToe_main()
                    break
                else:
                    print("Invalid Selection Defaulting to Alpha Beta Pruning algorithm.\n")
                    ttt.TicTacToe_main()
                    break           
            except ValueError:
                print("Invalid input, Defaulting to Alpha Beta Pruning algorithm.\n")
                algorithm = 2
                break

    if game == 2:  
        print(f"Setting up Nim")
        while True:
            try:
                algorithm = int(input("Would you like to play with: \n Complete Tree Search: 1 or \n Alpha Beta Pruning = 2?\n\nEnter Algorithm Number: "))
                if algorithm == 1:
                    print("Starting Nim with Complete Tree Search...\n")
                    NimC.Nim_main()
                    break
                elif algorithm == 2:                    
                    print("Starting Nim with Alpha Beta Pruning...\n")
                    Nim.Nim_main()
                    break
                else:
                    print("Invalid Selection Defaulting to Alpha Beta Pruning algorithm.\n")
                    ttt.TicTacToe_main()
                    break           
            except ValueError:
                print("Invalid input, Defaulting to Alpha Beta Pruning algorithm.\n")
                algorithm = 2
                break
 
    if game == 3: 
        print("Setting up Tiger vs Dogs")
        while True: 
            try:
                print("\nStarting Tiger vs Dogs with Alpha Beta Pruning\n")
                Td.Tiger_vs_Dogs_main()
                break
            except Exception as e:
                print(f"There was an error: {e}")
                break


    if game == 4: 
        print("Setting Up Connect 4")
        while True: 
            try:
                print("\nStarting Connect 4 with Alpha Beta Pruning\n")
                c4.connect4_main()
                break
            except Exception as e:
                print(f"There was an error: {e}")
                break        