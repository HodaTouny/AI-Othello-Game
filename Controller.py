from Board import Board
from GameLogic import GameLogic


class GameController:
    def __init__(self):
        self.board = Board()
        self.game = GameLogic(self.board)
        self.difficulty = None

    def getPlayerName(self):
        name = input("Enter your name: ")
        return name

    def selectDifficulty(self):
        while True:
            print("Select the difficulty level:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            choice = input("Enter the number corresponding to your choice: ")
            if choice in ['1', '2', '3']:
                self.difficulty = int(choice)
                break
            else:
                print("Invalid input! Please enter a valid choice.")

    HumanDisks = 32
    ComputerDisks = 32

    def run(self):
        player_name = self.getPlayerName()
        print(f"Welcome, {player_name}!")
        self.selectDifficulty()  # Prompt the user to select the difficulty level
        print(
            f"You've selected the difficulty level: {'Easy' if self.difficulty == 1 else 'Medium' if self.difficulty == 2 else 'Hard'}")
        player = 2
        while True:
            player_choice = []
            self.board.display()
            valid_moves_human = self.game.getAllValidMoves(self.board, 1)
            valid_moves_computer = self.game.getAllValidMoves(self.board, 2)

            if not valid_moves_computer and not valid_moves_human:
                player_score = self.game.calculatePlayerScore(1)
                computer_score = self.game.calculatePlayerScore(2)
                result = self.checkWinner(valid_moves_human, valid_moves_computer, player_score, computer_score,
                                          player_name)
                print(result)
                break

            if player == 1:
                print("It's your turn!")
                if not valid_moves_human:
                    print("You have no valid moves. Skipping Your turn.....")
                    player = 3 - player
                    continue
                print("Please choose one from your valid moves: ", valid_moves_human)
                while True:
                    try:
                        row = int(input("Enter row number: "))
                        col = int(input("Enter column number: "))
                        if [row, col] in valid_moves_human:
                            player_choice.append(row)
                            player_choice.append(col)
                            break
                        else:
                            print("Invalid move, please enter a new one.")
                    except ValueError:
                        print("Invalid input! Please enter integer numbers only for row and column fields.")

            else:
                print("It's Computer's turn!")
                if not valid_moves_computer:
                    print("Computer has no valid moves. Skipping Computer's turn.....")
                    player = 3 - player
                    continue
                depth = (self.difficulty - 1) * 2 + 1
                alpha = float('-inf')
                beta = float('inf')
                best_next_pos = self.game.alpha_beta_pruning(self.board, player, depth, alpha, beta, True)
                player_choice, _ = best_next_pos
                print("Computer's move:", player_choice)
            if player_choice:
                self.board.make_move(player_choice[0], player_choice[1], player)
                self.game.updateBoard(player, self.board, player_choice)
            else:
                self.board.display()

            player = 3 - player
