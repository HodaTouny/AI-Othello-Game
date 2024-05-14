from Board import Board


class GameLogic:
    def __init__(self, board):
        self.board = board

    # Return The All Valid Moves for the player by checking it is withing board boundries and
    # it is not occupied & it can out-flank
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

    # Check if it The Move can out-flank
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

    # Check if the move is valid
    def isValid(self, board, i, j, player):
        return 8 > i >= 0 and 8 > j >= 0 and board.GameBoard[i][j] == 0 and self.canOutFlank(board, i, j, player)

    # Computer Brain
    def alpha_beta_pruning(self, board, player, depth, alpha, beta, is_maximizing):
        if depth == 0:
            score = self.calculatePlayerScore(player)
            return None, score

        best_move = None
        best_score = float('-inf') if is_maximizing else float('inf')
        valid_moves = self.getAllValidMoves(board, player)

        for move in valid_moves:
            new_board = Board()
            new_board.GameBoard = [row[:] for row in board.GameBoard]
            new_board.make_move(move[0], move[1], player)
            _, score = self.alpha_beta_pruning(new_board, 3 - player, depth - 1, alpha, beta, not is_maximizing)

            if is_maximizing:
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
            
        return best_move, best_score

    # Calculate Player Score
    def calculatePlayerScore(self, player):
        score = 0
        for i in range(8):
            for j in range(8):
                if self.board.GameBoard[i][j] == player:
                    score += 1
        return score

    # The Utility Function
    def checkWinner(self, score_human, score_computer, human_name):
        if score_human > score_computer:
            return f"{human_name} wins!"
        elif score_human < score_computer:
            return "Computer wins!"
        else:
            return "draw!"
