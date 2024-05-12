import random


class Board:
    def __init__(self):
        self.size = 8
        self.GameBoard = [[0] * self.size for _ in range(self.size)]
        self.GameBoard[3][3] = 1
        self.GameBoard[3][4] = 2
        self.GameBoard[4][3] = 2
        self.GameBoard[4][4] = 1

    def display(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.GameBoard[i][j] == 1:
                    print('W', end=" ")
                elif self.GameBoard[i][j] == 2:
                    print('B', end=" ")
                else:
                    print('*', end=" ")
            print()

    def make_move(self, row, col, player):
        if self.GameBoard[row][col] == 0:
            self.GameBoard[row][col] = player
            return True

        return False


class GameController:
    def __init__(self, board):
        self.board = board

    def getAllValidMoves(self, board, player):
        valid_moves = []
        opponent = 3 - player

        for i in range(8):
            for j in range(8):
                if board.GameBoard[i][j] == opponent:
                    if self.isValid(board, i - 1, j, player) and [i - 1, j] not in valid_moves:
                        valid_moves.append([i - 1, j])
                    if self.isValid(board, i + 1, j, player) and [i + 1, j] not in valid_moves:
                        valid_moves.append([i + 1, j])
                    if self.isValid(board, i, j - 1, player) and [i, j - 1] not in valid_moves:
                        valid_moves.append([i, j - 1])
                    if self.isValid(board, i, j + 1, player) and [i, j + 1] not in valid_moves:
                        valid_moves.append([i, j + 1])
                    if self.isValid(board, i + 1, j + 1, player) and [i + 1, j + 1] not in valid_moves:
                        valid_moves.append([i + 1, j + 1])
                    if self.isValid(board, i - 1, j - 1, player) and [i - 1, j - 1] not in valid_moves:
                        valid_moves.append([i - 1, j - 1])
                    if self.isValid(board, i + 1, j - 1, player) and [i + 1, j - 1] not in valid_moves:
                        valid_moves.append([i + 1, j - 1])
                    if self.isValid(board, i - 1, j + 1, player) and [i - 1, j + 1] not in valid_moves:
                        valid_moves.append([i - 1, j + 1])

        return valid_moves

    def canOutFlank(self, board, i, j, player):
        opponent = 3 - player
        count = 0
        for k in range(j + 1, 8):
            if board.GameBoard[i][k] == opponent:
                count += 1
            elif board.GameBoard[i][k] == player:
                if count > 0:
                    return True
                else:
                    break
            else:
                break

        count = 0
        for k in range(j - 1, -1, -1):
            if board.GameBoard[i][k] == opponent:
                count += 1
            elif board.GameBoard[i][k] == player:
                if count > 0:
                    return True
                else:
                    break
            else:
                break

        count = 0
        for k in range(i + 1, 8):
            if board.GameBoard[k][j] == opponent:
                count += 1
            elif board.GameBoard[k][j] == player:
                if count > 0:
                    return True
                else:
                    break
            else:
                break

        count = 0
        for k in range(i - 1, -1, -1):
            if board.GameBoard[k][j] == opponent:
                count += 1
            elif board.GameBoard[k][j] == player:
                if count > 0:
                    return True
                else:
                    break
            else:
                break

        return False

    def isValid(self, board, i, j, player):
        return 8 > i >= 0 and 8 > j >= 0 and board.GameBoard[i][j] == 0 and self.canOutFlank(board, i, j, player)

    def flipDisk(self, disks, player, board):
        for k in range(len(disks)):
            row, col = disks[k]
            board.GameBoard[row][col] = player

    def updateBoard(self, player, board, playerChoice):
        opponent = 3 - player
        flippedTiles = []
        i = playerChoice[0]
        j = playerChoice[1]
        for k in range(j + 1, 8):
            if board.GameBoard[i][k] == opponent:
                flippedTiles.append([i, k])
            elif board.GameBoard[i][k] == player:
                if flippedTiles:
                    self.flipDisk(flippedTiles, player, board)
            else:
                break

        flippedTiles.clear()
        for k in range(j - 1, -1, -1):
            if board.GameBoard[i][k] == opponent:
                flippedTiles.append([i, k])
            elif board.GameBoard[i][k] == player:
                if flippedTiles:
                    self.flipDisk(flippedTiles, player, board)
            else:
                break
        flippedTiles.clear()
        for k in range(i + 1, 8):
            if board.GameBoard[k][j] == opponent:
                flippedTiles.append([k, j])
            elif board.GameBoard[k][j] == player:
                if flippedTiles:
                    self.flipDisk(flippedTiles, player, board)
            else:
                break

        flippedTiles.clear()
        for k in range(i - 1, -1, -1):
            if board.GameBoard[k][j] == opponent:
                flippedTiles.append([k, j])
            elif board.GameBoard[k][j] == player:
                if flippedTiles:
                    self.flipDisk(flippedTiles, player, board)
            else:
                break

    def alpha_beta_pruning(self, board, player, depth, alpha, beta):
        best_score = float('-inf') if player == 1 else float('inf')
        best_move = None

        valid_moves = self.getAllValidMoves(board, player)

        for move in valid_moves:
            new_board = Board()
            new_board.GameBoard = [row[:] for row in board.GameBoard]  # Copy the game board
            new_board.make_move(move[0], move[1], player)
            score = self.minimax(new_board, player, depth - 1, alpha, beta, False)

            if player == 1:
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)

            if beta <= alpha:
                break

        return best_move

    def minimax(self, board, player, depth, alpha, beta, is_maximizing):
        if depth == 0:
            return self.calculatePlayerScore(1) - self.calculatePlayerScore(2)

        if is_maximizing:
            max_eval = float('-inf')
            valid_moves = self.getAllValidMoves(board, player)

            for move in valid_moves:
                new_board = Board()
                new_board.GameBoard = [row[:] for row in board.GameBoard]  # Copy the game board
                new_board.make_move(move[0], move[1], player)
                eval = self.minimax(new_board, 3 - player, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval
        else:
            min_eval = float('inf')
            valid_moves = self.getAllValidMoves(board, player)

            for move in valid_moves:
                new_board = Board()
                new_board.GameBoard = [row[:] for row in board.GameBoard]  # Copy the game board
                new_board.make_move(move[0], move[1], player)
                eval = self.minimax(new_board, 3 - player, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval

    def calculatePlayerScore(self, player):
        score = 0
        for i in range(8):
            for j in range(8):
                if self.board.GameBoard[i][j] == player:
                    score += 1
        return score


class View:
    def __init__(self):
        self.board = Board()
        self.game = GameController(self.board)
        self.difficulty = None  # Initialize the difficulty level

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
                    row = int(input("Enter row number: "))
                    col = int(input("Enter column number: "))
                    if [row, col] in valid_moves_human:
                        player_choice.append(row)
                        player_choice.append(col)
                        break
                    else:
                        print("Invalid move, please enter a new one.")

            else:
                print("It's Computer's turn!")
                if not valid_moves_computer:
                    print("Computer has no valid moves. Skipping Computer's turn.....")
                    player = 3 - player
                    continue
                depth = (self.difficulty - 1) * 2 + 1
                alpha = float('-inf')
                beta = float('inf')
                best_next_pos = self.game.alpha_beta_pruning(self.board, player, depth, alpha, beta)
                print("Computer's move:", best_next_pos)
                player_choice = best_next_pos

            if player_choice:
                self.board.make_move(player_choice[0], player_choice[1], player)
                self.game.updateBoard(player, self.board, player_choice)
            else:
                self.board.display()

            player = 3 - player

    def checkWinner(board, valid_moves_human, valid_moves_computer, score_human, score_computer, human_name):
        if not valid_moves_human and not valid_moves_computer:
            if score_human > score_computer:
                return f"{human_name} wins!"
            elif score_human < score_computer:
                return "Computer wins!"
            else:
                return "draw!"

view = View()
view.run()
