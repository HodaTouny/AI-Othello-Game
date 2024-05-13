class Board:
    # initialize The Board
    def __init__(self):
        self.size = 8
        self.GameBoard = [[0] * self.size for _ in range(self.size)]
        self.GameBoard[3][3] = 1
        self.GameBoard[3][4] = 2
        self.GameBoard[4][3] = 2
        self.GameBoard[4][4] = 1

    # Display The Board
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

    # Write User Move on the Board
    def make_move(self, row, col, player):
        if self.GameBoard[row][col] == 0:
            self.GameBoard[row][col] = player
            return True

        return False

    # Update Board By Flipping Disks
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
