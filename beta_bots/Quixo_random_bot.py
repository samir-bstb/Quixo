import random
#The including bot was also for testing, this is an AI vs human game created to understand the game

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
        print("Then type the direction you want to move the piece (L for left, R for right, U for up, D for down).")
        self.print_board(self.board)

        while not self.check_winner(self.board, self.player_symbol) and not self.check_winner(self.board, self.computer_symbol) and not self.check_draw(self.board):
            while True:
                x, y = map(int, input("Enter your move (row and column): ").split())
                if self.board[x][y] == self.computer_symbol:
                    print("You cannot move the computer's piece. Try again.")
                elif (x, y) in self.forbidden_moves:
                    print("Forbidden move, try again.")
                else:
                    break
            direction = self.get_valid_direction(x, y)

            if (x, y) in self.forbidden_moves:
                print("Forbidden move, try again")
                continue

            if self.board[x][y] == '' or self.board[x][y] == self.player_symbol:
                self.board[x][y] = self.player_symbol
                self.move_to_pos(direction, x, y)
                self.print_board(self.board)

                if self.check_winner(self.board, self.player_symbol):
                    print("You win!")
                    break

                if self.check_draw(self.board):
                    print("It's a draw!")
                    break

                if self.computer_move():
                    break

            else:  
                print("Computer's turn to move its piece.")
                if self.computer_move_from_position(x, y, direction):
                    break

    def computer_move(self):
        possible_moves  = [(i, j) for i in range(5) for j in range(5) if (self.board[i][j] == '' or self.board[i][j] == self.computer_symbol) and (i, j) not in self.forbidden_moves]
        if not possible_moves :
            return False

        x, y = random.choice(possible_moves )
        direction = self.get_random_valid_direction(x, y)
        self.board[x][y] = self.computer_symbol
        self.move_to_pos(direction, x, y)
        print(f"Computer's move: ({x},{y}) in direction: {direction}")
        self.print_board(self.board)
        
        
        if self.check_winner(self.board, self.computer_symbol):
            print("You lose!")
            return True
        elif self.check_draw(self.board):
            print("It's a draw!")
            return True
        return False

    def computer_move_from_position(self, x, y, direction):
        self.move_to_pos(direction, x, y)
        self.print_board(self.board)

        if self.check_winner(self.board, self.computer_symbol):
            print("You lose!")
            return True
        elif self.check_draw(self.board):
            print("It's a draw!")
            return True
        return False

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
            self.move_left(x, y)
        elif direction == 'r':
            self.move_right(x, y)
        elif direction == 'u':
            self.move_up(x, y)
        elif direction == 'd':
            self.move_down(x, y)
        else:
            print("Invalid direction")

    def get_valid_direction(self, x, y):
        while True:
            direction = input("Enter direction: ").lower()
            if self.is_valid_direction(direction, x, y):
                return direction
            else:
                print("Oops! You can't do that")

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

    def get_random_valid_direction(self, x, y):
        directions = []
        if y > 0:
            directions.append('l')
        if y < 4:
            directions.append('r')
        if x > 0:
            directions.append('u')
        if x < 4:
            directions.append('d')
        return random.choice(directions)

    def move_right(self, x, y):
        row = self.board[x]
        aux = row.pop(y)
        row.append(aux)

    def move_left(self, x, y):
        row = self.board[x]
        aux = row.pop(y)
        row.insert(0, aux)

    def move_down(self, x, y):
        col = [self.board[i][y] for i in range(5)]
        aux = col.pop(x)
        col.append(aux)
        for i in range(5):
            self.board[i][y] = col[i]

    def move_up(self, x, y):
        col = [self.board[i][y] for i in range(5)]
        aux = col.pop(x)
        col.insert(0, aux)
        for i in range(5):
            self.board[i][y] = col[i]

board = [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]

Q = Quixo(board)
Q.play()
