import random
#This program was made to test the moves of the pices on the board and their behavior

class Quixo:
    def __init__(self, board):
        self.board = board
        self.forbidden_moves = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
        self.player_symbol, self.computer_symbol = self.assign_symbols()

    def assign_symbols(self):
        if random.choice([True, False]):
            return 'X', 'O'
        else:
            return 'O', 'X'

    def play(self):
        print("Welcome to Quixo!")
        print(f"You are playing as '{self.player_symbol}'. ")
        print("Enter your piece of choice by specifying the row and column numbers (0-4).")
        print("Then type the direction you want to move the piece")
        print("L for left, R for right, U for up or D for down")
        self.print_board(self.board)

        while not self.check_winner(self.board, self.player_symbol) and not self.check_winner(self.board, self.computer_symbol) and not self.check_draw(self.board):
            while True:
                x, y = map(int, input("Enter your move (row and column): ").split())
                if self.board[x][y] == self.computer_symbol:
                    print("You can't move that piece, choose another one")
                elif (x, y) in self.forbidden_moves:
                    print("Forbidden move, try again")
                else:
                    break
            direction = self.get_valid_direction(x,y)

            if (x, y) in self.forbidden_moves:
                print("Forbidden move, try again")
                continue

            if self.board[x][y] == '':
                self.board[x][y] = self.player_symbol
                self.print_board(self.board)
                print()
                self.move_to_pos(direction, x, y)
                self.print_board(self.board)
                
                if self.check_winner(self.board, self.player_symbol):
                    print("You win!")
                    break
                elif self.check_draw(self.board):
                    print("It's a draw!")
                    break
                best_move = self.get_best_move(self.board)
                self.board[best_move[0]][best_move[1]] = self.computer_symbol
                print("Computer's move:")
                self.print_board(self.board)
                if self.check_winner(self.board, self.computer_symbol):
                    print("You lose!")
                    break
                elif self.check_draw(self.board):
                    print("It's a draw!")
                    break
            elif self.board[x][y] == self.player_symbol:
                self.move_to_pos(direction, x, y)
                self.print_board(self.board)

                if self.check_winner(self.board, self.computer_symbol):
                    print("You Lose! :(")
                    break
                
                if self.check_winner(self.board, self.player_symbol):
                    print("You win!")
                    break
                
                elif self.check_draw(self.board):
                    print("It's a draw!")
                    break
                #Missing: after user's move, the computer has to make its move, otherwise the user is able to move again
            else: #the cell is occupied by the computer
                pass

    '''
    def minimax_alpha_beta(self, board, depth, is_maximizing, alpha, beta):
        if self.check_winner(board, self.player_symbol):
            return -1
        elif self.check_winner(board, self.computer_symbol):
            return 1
        elif self.check_draw(board):
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(5):
                for j in range(5):
                    if self.board[i][j] == '':
                        board[i][j] = self.computer_symbol
                        score = self.minimax_alpha_beta(board, depth+1, False, alpha, beta)
                        board[i][j] = ''
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for i in range(5):
                for j in range(5):
                    if board[i][j] == '':
                        board[i][j] = self.player_symbol
                        score = self.minimax_alpha_beta(board, depth+1, True, alpha, beta)
                        board[i][j] = ''
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score

    def get_best_move(self, board):
        best_score = -float('inf')
        best_move = ()
        alpha = -float('inf')
        beta = float('inf')
        for i in range(5):
            for j in range(5):
                if board[i][j] == '':
                    board[i][j] = self.computer_symbol
                    score = self.minimax_alpha_beta(board, 0, False, alpha, beta)
                    board[i][j] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move '''

    def check_winner(self, board, player):
        for i in range(5):
            if all([board[i][j] == player for j in range(5)]):
                return True
            if all([board[j][i] == player for j in range(5)]):
                return True
        if all([board[i][i] == player for i in range(5)]) or all([board[i][4 - i] == player for i in range(5)]):
            return True
        return False

    def check_draw(self, board):
        return all([all([cell != '' for cell in row]) for row in board]) 

    def print_board(self, board):
        print("   0   1   2   3   4")
        print(" +---+---+---+---+---+")
        for i, row in enumerate(board):
            row_str = " | ".join(cell if cell else ' ' for cell in row)
            print(f"{i}| {row_str} |")
            print(" +---+---+---+---+---+")

    def move_to_pos(self, direction, x, y):
        if direction == 'l':
            self.move_left(x,y)
        elif direction == 'r':
            self.move_right(x,y)
        elif direction == 'u':
            self.move_up(x,y)
        elif direction == 'd':
            self.move_down(x,y)
        else:
            print("Invalid direction")

    def get_valid_direction(self, x, y):
        while True:
            direction = input("Enter direction: ").lower()
            if self.is_valid_direction(direction, x, y):
                return direction
            else:
                print("Ooops! You can't do that")

    def is_valid_direction(self, direction, x, y):
        if direction == 'l' and y > 0:
            return True
        if direction == 'r' and y < 4:
            return True
        if direction == 'u' and x > 0:
            return True
        if direction == 'd' and x < 4:
            return True
        return False

    def move_right(self, x, y):
        row = self.board[x]
        aux = row.pop(y)
        row.append(aux)

    def move_left(self, x, y):
        row = self.board[x]
        aux = row.pop(y)
        row.insert(0, aux)

    def move_down(self, x, y):
         col = [row[y] for row in self.board] 
         aux = col.pop(x)
         col.append(aux)
         for i in range(5):
             self.board[i][y] = col[i]

    def move_up(self, x, y):
        col = [row[y] for row in self.board]
        aux = col.pop(x)
        col.insert(0, aux)
        for i in range(5):
            self.board[i][y] = col[i]

    

#board = [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]
board = [['O', 'X', '', '', ''], 
         ['', 'X', 'X', 'X', ''], 
         ['O', '', '', '', 'O'], 
         ['', '', '', '', ''], 
         ['', 'O', 'X', '', '']]

Q = Quixo(board)
Q.play()
