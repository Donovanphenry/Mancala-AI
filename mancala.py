
import sys
import os
from time import time
from io import StringIO

#Varialbes for mancala pit and depth
#each player has 7 pits, 6 small ones, one Mancala pit (to score)
MANCALA_PIT = 7
DEPTH = 5

#defining the class to represent the board
class Board:

    #some self representation functions
    def __str__(self, *args, kwargs):
        return str(self.board)

    def __repr__(self, *args, **kwargs):
        return "Board%s" % self.__str__()

    #defining property class to modify self object (setting points for player 1 and player 2)
    @property
    def player1_points(self):
        if self.no_moves_remaining():
            return sum(self.board[1:8])
        else:
            return self.board[7]

    @property
    def player2_points(self):
        if self.no_moves_remaining():
            return self.board[0] + sum(self.board[8:])
        else:
            return self.board[0]    
    #the above functions are defined to make it easier to print, and update the board as moves are made
    
    
    #initializing the board
    def __init__(self, board=None):
        if board is not None:
            self.board = board.board[:]
            self.reversed = board.reversed
        else:
            self.board = [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]
            self.reversed = False            

    #define a function to check if moves can be made
    def no_moves_remaining(self):
        if any(self.board[8:]) == False or any(self.board[1:7]) == False:
            return True
        return False
    
    def no_moves_remaining_array(self, arr):
        if any(arr[8:]) == False or any(arr[1:7]) == False:
            return True
        return False

    #define this function to find all possible moves given the current board state.
    #this function will help you determine the best possible move when using min_max 
    #and alpha_beta.
    def find_moves_player1(self, state, states, curr_path, path_map, curr_depth = 0, max_depth = 3):
        if self.no_moves_remaining_array(state):
            return [state], path_map
        if curr_depth >= max_depth:
            return states, path_map
        
        states.append(state)
        if curr_path not in path_map:
            path_map[curr_path] = {}
            path_map[curr_path]['adj'] = []

        for i in range(8, 14):
            next_path = curr_path + str(i) + ';'
            no_stones = state[i] == 0
            t = self.update_board(i, board=state.copy())
            next_move, next_turn = None, None
            if no_stones == False:
                next_move, next_turn = self.update_board(i, board=state.copy())

            if next_move != None and no_stones == False:
                path_map[curr_path]['adj'].append(next_path)
                path_map[next_path] = {}
                path_map[next_path]['scores'] = next_move[7] - next_move[0]
                path_map[next_path]['parent'] = curr_path
                path_map[next_path]['adj'] = []
                if next_turn == 1:
                    self.find_moves_player1(next_move, states, next_path, path_map, curr_depth = curr_depth + 1, max_depth = max_depth)
                else: 
                    self.find_moves_player2(next_move, states, next_path, path_map, curr_depth = curr_depth + 1, max_depth = max_depth)
        return states, path_map
    def find_moves_player2(self, state, states, curr_path, path_map, curr_depth = 0, max_depth = 3):
        if self.no_moves_remaining_array(state):
            return [state], path_map
        if curr_depth >= max_depth:
            return states, path_map
        
        states.append(state)
        if curr_path not in path_map:
            path_map[curr_path] = {}
            path_map[curr_path]['adj'] = []
        
        for i in range(1, 7):
            next_path = curr_path + str(i) + ';'
            no_stones = state[i] == 0
            next_move, next_turn = None, None
            if no_stones == False:
                next_move, next_turn = self.update_board(i, board=state.copy())

            if next_move != None and no_stones == False:
                path_map[curr_path]['adj'].append(next_path)
                path_map[next_path] = {}
                path_map[next_path]['scores'] = next_move[7] - next_move[0]
                path_map[next_path]['parent'] = curr_path
                path_map[next_path]['adj'] = []
                if next_turn == 1:
                    self.find_moves_player1(next_move, states, next_path, path_map, curr_depth = curr_depth + 1, max_depth = max_depth)
                else: 
                    self.find_moves_player2(next_move, states, next_path, path_map, curr_depth = curr_depth + 1, max_depth = max_depth)
        return states, path_map

    def find_moves(self, turn, root=None, max_depth = 3):
        if root is None:
            root = 'null;'
        _, path_map = None, None
        if turn == 2:
            _, path_map = self.find_moves_player2(self.board.copy(), [], root, {}, max_depth = max_depth)
        else:
            _, path_map = self.find_moves_player1(self.board.copy(), [], root, {}, max_depth = max_depth)

        if 'scores' not in path_map[root]:
            path_map[root]['scores'] = (self.board[7], self.board[0])

        return path_map


    #define helper functions to help with "update_board()" function in the space below, before the "update_board()" function
    def is_valid_choice(self, n, board):
        if board is None:
            board = self.board
        if n <= 0 or n == 7 or n > len(board) or board[n] == 0:
            return False
        return True

    #definie the "update_board()" function here.
    #this function updates the board using the parameter "n" passed to it.
    #using "n" as the players pit location, take the stones from that location,
    #and update the board according to the rules (counterclockwise).
    #if helper functions are needed, use the space above to define them.
    def update_board(self, n, board=None):
        # print("in update_board")
        player = 2 if n < 7 else 1
        next_turn = 1 if player == 2 else 2
        if board is None:
            board = self.board
        if n == 0 or n == 7:
            return None, next_turn
        elif self.board[n] == 0:
            return None, next_turn

        index = n
        stones = board[index]
        if n != 0:
            board[index] = 0
            index -= 1

        while stones != 0:
            opp_index = 14 - index
            if index != 0 and index != 7 and stones == 1 and board[index] == 0 and board[opp_index] != 0:
                if index < 7 and player == 2:
                    board[0] += board[opp_index] + stones
                    board[opp_index] = 0
                    break
                elif index > 7 and player == 1:
                    board[7] += board[opp_index] + stones
                    board[opp_index] = 0
                    break
            if not (player == 1 and index == 0) and not (player == 2 and index == 7):
                board[index] += 1
                stones -= 1
            if (index == 0 or index == 7) and stones == 0:
                next_turn = 1 if player == 1 else 2
            index -= 1
            if index == -1:
                index = len(board) - 1
        
        if self.no_moves_remaining_array(board):
            for x, y in zip(range(1, 7), range(8, 14)):
                board[0] += board[x]
                board[x] = 0
                board[7] += board[y]
                board[y] = 0
        return board, next_turn

    def max_value(self, next_node, path_map):
        if path_map[next_node]['adj'] == []:
            return path_map[next_node]['scores'], next_node
        
        v = -1 * float('inf')
        max_path = next_node

        for action in path_map[next_node]['adj']:
            u, u_path = self.min_value(action, path_map)
            v = v if v > u else u
            max_path = max_path if v > u else u_path

        return v, max_path
    
    def min_value(self, next_node, path_map):
        if path_map[next_node]['adj'] == []:
            return path_map[next_node]['scores'], next_node

        v = float('inf')
        min_path = next_node

        for action in path_map[next_node]['adj']:
            u, u_path = self.max_value(action, path_map)
            v = v if v < u else u
            min_path = min_path if v < u else u_path

        return v, min_path

    #define the min_max function below
    #the starter code defines it with self and depth=3. 
    #Add additional parameters if necessary
    def min_max(self, curr_root, curr_player, depth=3):
        path_map = self.find_moves(curr_player, root = curr_root, max_depth = depth)
        path_iter = ''
        if curr_player == 1:
            _, path_iter = self.max_value(curr_root, path_map)
        else:
            _, path_iter = self.min_value(curr_root, path_map)
        mp_arr = path_iter.split(';')
        mp_arr.pop(0)
        mp_arr.pop()
        print(f'------------------------------------------\nPlayer {curr_player} chooses {mp_arr[0]}')
        curr_root = mp_arr[0] + ';'

        return int(mp_arr[0])

    def ab_min_val(self, node, path_map, alpha, beta):
        if path_map[node]['adj'] == []:
            return path_map[node]['scores'], node
        
        v = float('inf')
        min_path = node

        for action in path_map[node]['adj']:
            u, u_path = self.ab_max_val(action, path_map, alpha, beta)
            v = min(u, v)
            min_path = min_path if v < u else u_path

            if v <= alpha:
                return v, min_path
            beta = min(v, beta)
        
        return v, min_path

    def ab_max_val(self, node, path_map, alpha, beta):
        if path_map[node]['adj'] == []:
            return path_map[node]['scores'], node
        
        v = -1 * float('inf')
        max_path = node

        for action in path_map[node]['adj']:
            u, u_path = self.ab_min_val(action, path_map, alpha, beta)
            v = max(u, v)
            max_path = max_path if v > u else u_path

            if v >= beta:
                return v, max_path
            alpha = max(alpha, v)
        
        return v, max_path

    #define the alpha beta pruning function to minimize/maximize.
    #the starter code defines it with self, depth=3, alpha=-999, beta=+999.
    #add more parameters if necessary
    #you need to call mim_max here to get the best value
    def alpha_beta(self, curr_root, curr_player, depth=3, alpha=-999, beta=+999):
        path_map = self.find_moves(curr_player, root = curr_root, max_depth = depth)
        v, path_iter = None, ''
        if curr_player == 1:
            v, path_iter = self.ab_max_val(curr_root, path_map, alpha, beta)
        else:
            v, path_iter = self.ab_min_val(curr_root, path_map, alpha, beta)
        mp_arr = path_iter.split(';')
        mp_arr.pop(0)
        mp_arr.pop()
        print(f'------------------------------------------\nPlayer {curr_player} chooses {mp_arr[0]}')
        curr_root = mp_arr[0] + ';'

        return int(mp_arr[0])
    
    #This function tells you how to caclulate the heuristic score.
    #This should work, changes are not necessary.
    def calculate_heurestic_score(self):
        if not self.reversed:
            return self.player1_points - self.player2_points
        else:
            return self.player2_points - self.player1_points

    #define more helper functions to print current board state here
    def print(self):
        print("         ", end="")
        print(*["%2d" % x for x in reversed(self.board[8:])], sep="|")
        print(
            "P2 --- %2d                  %2d --- P1"
            % (self.player2_points, self.player1_points)
        )
        print("         ", end="")
        print(*["%2d" % x for x in self.board[1:7]], sep="|")
    
def is_int(n):
    try:
        return float(str(n)).is_integer()
    except:
        return False

#this function defines an object of class Board
#to implement: set the board , according to the starting player (P1 or P2),
#caclulate best moves for players 1 and 2.
#Update the board according to the best move.
#Keep iterating for up to 15 moves total (both players combined) in the future,
#or until the game ends.
def play_mancala(initial_board=None, starting_player=1, human_player = 0):
    board = initial_board
    if initial_board is None:
        initial_board = Board()
    board = Board(board=initial_board)

    print('==================Starting standard minimax version==================')
    board.print()
    moves_made = []
    curr_player = int(starting_player)
    curr_root = 'null;'
    turn_count = 0
    while board.no_moves_remaining() == False and turn_count < 15:
        if curr_player != human_player:
            move = board.min_max(curr_root, curr_player, depth = 6)
            _, curr_player = board.update_board(move)
        else:
            move = int(input('Select a move: '))
            ret_board, curr_player = board.update_board(move)
            while ret_board == None:
                move = int(input("Error: Invalid move. Re-enter: "))
                ret_board, curr_player = board.update_board(move)

        curr_root = str(move) + ';'
        moves_made.append(move)
        board.print()
        turn_count += 1
    print('moves_made = ', moves_made)
    
    print('==================Standard game over. Starting minimax with alpha-beta pruning version==================')

    board = Board()
    board.print()
    moves_made = []
    curr_player = int(starting_player)
    curr_root = 'null;'
    turn_count = 0
    while board.no_moves_remaining() == False and turn_count < 15:
        if curr_player != human_player:
            move = board.alpha_beta(curr_root, curr_player, depth = 4)
            _, curr_player = board.update_board(move)
        else:
            move_str = input('Select a move: ')
            while is_int(move_str) == False:
                move_str = input('Error: Invalid Selection. Move must be an integer. Re-enter: ')

            move = int(move_str)
            ret_board, curr_player = board.update_board(move)
            while ret_board == None:
                move = int(input("Error: Invalid move. Re-enter: "))
                ret_board, curr_player = board.update_board(move)

        curr_root = str(move) + ';'
        moves_made.append(move)
        board.print()
        turn_count += 1
    print('moves_made = ', moves_made)
    print('==================Alpha-Beta pruning game over==================')
#main is defined here. it takes starting player from the commmand line,
#and calls play_mancala. Initial player is int, either 1 or 2.
#Note: for testing, you can define an initial board here and pass it to
#play_mancala to test different starting conditions.
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Error: Invalid number of command-line arguments. Requires 2. First is which player starts, second is which player the human is. Anything other than 1 or 2 pits two AI against each other')
    elif is_int(sys.argv[1]) == False or is_int(sys.argv[2]) == False:
        print('Error: Both command line args must be integers.')
    else:
        player_choice = sys.argv[1]
        print("player choice: ", player_choice)

        default_board = None
        
        human = int(sys.argv[2])
        play_mancala(initial_board = default_board, starting_player = player_choice, human_player = human)