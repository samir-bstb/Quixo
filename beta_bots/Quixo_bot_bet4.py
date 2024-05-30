import random
import copy

class QuixoBot:
    def _init_(self, symbol):
        self.name = "pancho"
        self.symbol = symbol

    def get_possible_moves(self, board):
        possible_moves = []
        size = len(board)

        # Check the top and bottom rows
        for j in range(size):
            for i in [0, size - 1]:
                if board[i][j] == 0 or board[i][j] == self.symbol:
                    if i > 0:
                        possible_moves.append((i, j, 'up'))
                    if i < size - 1:
                        possible_moves.append((i, j, 'down'))

        # Check the left and right columns
        for i in range(1, size - 1):
            for j in [0, size - 1]:
                if board[i][j] == 0 or board[i][j] == self.symbol:
                    if j > 0:
                        possible_moves.append((i, j, 'left'))
                    if j < size - 1:
                        possible_moves.append((i, j, 'right'))

        return possible_moves

    def simulate_game(self, board, move):
        # Aplicamos el movimiento dado al tablero
        board = self.apply_move(board, move, self.symbol)

        # Alternamos entre los jugadores
        current_player = -self.symbol

        while True:
            # Generamos un movimiento al azar para el jugador actual
            possible_moves = self.get_possible_moves(board)
            random_move = random.choice(possible_moves)

            # Aplicamos el movimiento al tablero
            board = self.apply_move(board, random_move, current_player)

            # Comprobamos si el juego ha terminado
            winner = self.check_winner(board)
            if winner is not None:
                return winner

            # Cambiamos de jugador
            current_player = -current_player

    def play_turn(self, board):
        possible_moves = self.get_possible_moves(board)
        best_move = None
        best_wins = -1

        for move in possible_moves:
            wins = 0
            for _ in range(200):
                result = self.simulate_game(copy.deepcopy(board), move)
                if result == self.symbol:
                    wins += 1

            if wins > best_wins:
                best_wins = wins
                best_move = move

        # Aplicamos el mejor movimiento al tablero
        board = self.apply_move(board, best_move, self.symbol)

        return board

    def reset(self, symbol):
        self.symbol = symbol

    def apply_move(self, board, move, symbol):
        i, j, direction = move
        size = len(board)

        if direction == 'up':
            for k in range(i, 0, -1):
                board[k][j] = board[k - 1][j]
            board[0][j] = symbol

        elif direction == 'down':
            for k in range(i, size - 1):
                board[k][j] = board[k + 1][j]
            board[size - 1][j] = symbol

        elif direction == 'left':
            for k in range(j, 0, -1):
                board[i][k] = board[i][k - 1]
            board[i][0] = symbol

        elif direction == 'right':
            for k in range(j, size - 1):
                board[i][k] = board[i][k + 1]
            board[i][size - 1] = symbol

        return board

    def check_winner(self, board):
        size = len(board)

        # Check rows and columns
        for i in range(size):
            row_sum = sum(board[i])
            col_sum = sum(board[j][i] for j in range(size))
            if abs(row_sum) == size:
                return board[i][0]
            if abs(col_sum) == size:
                return board[0][i]

        # Check diagonals
        diag_sum1 = sum(board[i][i] for i in range(size))
        diag_sum2 = sum(board[i][size - i - 1] for i in range(size))
        if abs(diag_sum1) == size:
            return board[0][0]
        if abs(diag_sum2) == size:
            return board[0][size - 1]

        # No winner
        return None
