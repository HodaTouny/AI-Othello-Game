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


# ----------------------------------------------------------------------------------------- #

class View:
    def __init__(self):
        self.board = Board()
        self.game = GameController()

    def getPlayerName(self):
        name = input("Enter your name: ")
        return name

    def run(self):
        player_name = self.getPlayerName()
        print(f"Welcome, {player_name}!")
        player_choice = []
        player = 2
        while True:
            player_choice.clear()
            self.board.display()
            if player == 1:
                print("It's your turn!")
                valid_moves = self.game.getAllValidMoves(self.board, 1)
                print("please choose one from your valid moves: ", valid_moves)
                while True:
                    row = int(input("Enter row number: "))
                    col = int(input("Enter column number: "))
                    if [row, col] in valid_moves:
                        player_choice.append(row)
                        player_choice.append(col)
                        break
                    else:
                        print("invalid move, Enter new one ")

            else:
                # print("Computer's turn...")
                print("It's Computer's turn!")
                
            self.board.make_move(player_choice[0], player_choice[1], player)
            self.game.updateBoard(player, self.board, player_choice)

            player = 3 - player

    def calculatePlayerScore(self, player):
        score = 0
        for i in range(self.board.size):
            for j in range(8):
                if self.board.GameBoard[i][j] == player:
                    score += 1
        return score


# ----------------------------------------------------------------------------------------- #
class GameController:

    def getAllValidMoves(self, board, player):
        valid_moves = []
        opponent = 3 - player

        for i in range(8):
            for j in range(8):
                if board.GameBoard[i][j] == opponent:
                    if self.isValid(board, i - 1, j, player) and [i-1,j] not in valid_moves:
                        valid_moves.append([i - 1, j])
                    if self.isValid(board, i + 1, j, player) and [i+1,j] not in valid_moves:
                        valid_moves.append([i + 1, j])
                    if self.isValid(board, i, j - 1, player) and [i,j-1] not in valid_moves:
                        valid_moves.append([i, j - 1])
                    if self.isValid(board, i, j + 1, player) and [i,j+1] not in valid_moves:
                        valid_moves.append([i, j + 1])
                    if self.isValid(board, i + 1, j + 1, player) and [i+1,j+1] not in valid_moves:
                        valid_moves.append([i + 1, j + 1])
                    if self.isValid(board, i - 1, j - 1, player) and [i-1,j-1] not in valid_moves:
                        valid_moves.append([i - 1, j - 1])
                    if self.isValid(board, i + 1, j - 1, player) and [i+1,j-1] not in valid_moves:
                        valid_moves.append([i + 1, j - 1])
                    if self.isValid(board, i - 1, j + 1, player) and [i-1,j+1] not in valid_moves:
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

    def checkWinner(board, valid_moves_human, valid_moves_computer, score_human, score_computer, human_name):
        if valid_moves_human.empty and valid_moves_computer.empty:
            if score_human > score_computer:
                return f"{human_name} wins!"
            elif score_human < score_computer:
                return "Computer wins!"
            else:
                return "draw!"


view = View()
view.run()