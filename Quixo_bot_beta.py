class QuixoBot:
   
    def __init__(self, symbol):
        self.symbol = symbol
        self.name = ""
        self.forbidden_moves = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]

    # board es el estado actual del tablero. Sera una matriz de 5x5 que contiene
    # los siguientes numeros enteros.
    #  0 - blank cubit
    #  1 - X cubit
    # -1 - O cubit
    def play_turn(self, board):
        self.get_best_move(board)
        #apply the best move
        #return the new board

    def get_best_move(self, board):    
        best_score = -float('inf')
        best_move = ()
        alpha = -float('inf')
        beta = float('inf')
        for i in range(5):
            for j in range(5):
                if (i, j) not in self.forbidden_moves:
                    if board[i][j] == '':
                        #make copy here
                        board[i][j] = self.computer_symbol
                        #make move in the allowed directions from the copied state
                        score = self.minimax_alpha_beta(board, 0, False, alpha, beta)

                        #calculate the heuristic values of the posible moves 
                        #apply minimax
            
                        if score > best_score:
                            best_score = score
                            best_move = (i, j) #get the best move
                    if board[i][j] == self.symbol:
                        #make move in the allowed directions from the copied state
                        #obtain the heuristic values of the moves
                        #apply minimax
                        #get the best move
                        pass
        return best_move

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        pass
        
    def get_possible_moves(self, board):
        moves = []
        for i in range(5):
            for j in range(5):
                if (board[i][j] == '' or board[i][j] == self.computer_symbol) and (i, j) not in self.forbidden_moves:
                    moves.append((i, j))
        return moves     

    def __move_right(self, row, col, board):
        if col < 4:
            board[row][col] = self.symbol
            Row = board[row]
            aux = Row.pop(col)
            Row.append(aux)
            return board
        else:
            return False

    def __move_left(self, row, col, board):
        if col > 0:
            board[row][col] = self.symbol
            Row = self.board[row]
            aux = Row.pop(col)
            Row.insert(0, aux)
        else:
            return False

    def __move_down(self, row, col, board):
        if row < 4:
            board[row][col] = self.symbol
            Col = [row[col] for row in board] 
            aux = Col.pop(row)
            Col.append(aux)
            for i in range(5):
                self.board[i][col] = Col[i]
        else:
            return False

    def __move_up(self, row, col, board):
        if row > 0:
            board[row][col] = self.symbol
            Col = [row[col] for row in board]
            aux = Col.pop(row)
            Col.insert(0, aux)
            for i in range(5):
                self.board[i][col] = Col[i]   
        else:
            return False
    .
    def reset(self, symbol):
        pass

#board = [[0 for _ in range(5)] for _ in range(5)]
board = [[-1, 1, 0, 0,-1], 
         [ 0, 1, 1, 1, 0], 
         [-1, 0, 0, 0,-1], 
         [ 0, 0, 0, 0, 0], 
         [ 0,-1, 1, 0, 0]]

bot = QuixoBot(1)
print(board)
new_board = bot.play_turn(board)
