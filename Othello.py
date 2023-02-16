
import random
import numpy as np


#Code for modelling the Othello game and all the methods needed in the rest of the code

class Othello:
    
    def __init__(self):
        # initialize the board with starting pieces
        self.board = [[0 for _ in range(6)] for _ in range(6)]
        self.board[2][2] = self.board[3][3] = 1
        self.board[2][3] = self.board[3][2] = -1
        # 1  White, -1 Black
        self.turn = 1
      
    
    def display(self):
        # display the board 
        print("  0 1 2 3 4 5")
        for i in range(6):
            
            print(i, end=" ")
            for j in range(6):
                if self.board[i][j] == 1:
                    print("W ", end="")
                    
                elif self.board[i][j] == -1:
                    print("B ", end="")
                    
                else:
                    print("- ", end="")
                    
            print()
        print()
        return
        
        
    def get_turn(self):
        return self.turn 

    
    def get_board(self):
        return self.board

        
    def show_numbers(self):
        # display the board with numbers
        print("  0  1  2  3  4  5")
        for i in range(6):
            print(i, end=" ")
            for j in range(6):
                nombre = i*6+j
                if nombre//10 > 0:
                    print(i*6+j, end=" ")
                    
                else :
                    print(i*6+j, end="  ")
                    
            print()
        print()
        return
        
    
    def is_valid(self, x, y):
        # check if a move is valid
        if x < 0 or x > 5 or y < 0 or y > 5:
            # out of bounds
            return False
        if self.board[x][y] != 0:
            # already occupied
            return False
        
        # check all 8 directions
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            i, j = x + dx, y + dy
            if i < 0 or i > 5 or j < 0 or j > 5:
                # out of bounds
                continue
            if self.board[i][j] == -self.turn:
                # opponent's piece found
                while True:
                    i, j = i + dx, j + dy
                    if i < 0 or i > 5 or j < 0 or j > 5:
                        # out of bounds
                        break
                    if self.board[i][j] == 0:
                        # no more pieces to flip in this direction
                        break
                    if self.board[i][j] == self.turn:
                        # our piece found, the move is valid
                        return True
        return False

    
    def is_valid_board(self, board, turn, x, y):
        # check if a move is valid for a given board
        if x < 0 or x > 5 or y < 0 or y > 5:
            # out of bounds
            return False
        if board[x][y] != 0:
            # already occupied
            return False
        
        # check all 8 directions
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            i, j = x + dx, y + dy
            if i < 0 or i > 5 or j < 0 or j > 5:
                # out of bounds
                continue
            if board[i][j] == -turn:
                # opponent's piece found
                while True:
                    i, j = i + dx, j + dy
                    if i < 0 or i > 5 or j < 0 or j > 5:
                        # out of bounds
                        break
                    if board[i][j] == 0:
                        # no more pieces to flip in this direction
                        break
                    if board[i][j] == turn:
                        # our piece found, the move is valid
                        return True
        return False


    def valid_actions(self):
        # return a list of all valid moves
        actions = []
        for i in range(6):
            for j in range(6):
                if self.is_valid(i, j):
                    actions.append((i, j))
        return actions

    def valid_actions_mask(self):
        # return a board with 1 on all valid moves
        actions = self.valid_actions()
        mask = [[0 for _ in range(6)] for _ in range(6)]
        for x,y in actions:
            mask[x][y] = 1
        return mask
      
        
    def set_state(self, state):
        self.board = state
      
    
    def get_next_state(self, action):
        # if the action is valid, do the action and return the new board
        x, y = action 
        if self.is_valid(x,y):
            self.play(x,y)
            b = self.board            
        return self.board

    
    def valid_actions_board(self):
        valid_board = [[0 for _ in range(6)] for _ in range(6)]
        list_actions = self.valid_actions()
        for x, y in list_actions:
            valid_board[x][y] = 1
        return valid_board    
    
    
    def play(self, x, y):
        #play on the board the value x, y
        if not self.is_valid(x, y):
            # move is not valid
            return False

        self.board[x][y] = self.turn

        # flip pieces in all 8 directions
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            i, j = x + dx, y + dy
            if i < 0 or i > 5 or j < 0 or j > 5:
                # out of bounds
                continue
            if self.board[i][j] == -self.turn:
                # opponent's piece found
                i, j = i + dx, j + dy
                while i >= 0 and i <= 5 and j >= 0 and j <= 5 and self.board[i][j] == -self.turn:
                    i, j = i + dx, j + dy
                if i >= 0 and i <= 5 and j >= 0 and j <= 5 and self.board[i][j] == self.turn:
                    # our piece found, flip pieces in between
                    i, j = x + dx, y + dy
                    while self.board[i][j] == -self.turn:
                        self.board[i][j] = self.turn
                        i, j = i + dx, j + dy

        # switch turn
        self.turn = -self.turn
        return True
    
    
    def get_winner(self, player=1):
        #give the winner of the game
        if not self.is_game_over():
            return None 
        total = 0
        for i in range(6):
            for j in range(6):
                total += self.board[i][j]
                
        if total > 0:
            return player
        elif total < 0:
            return -player
        else:
            return 0
        return
    
    
    def is_game_over(self):
        #check if the game is over
        if not any([self.is_valid(i, j) for i in range(6) for j in range(6)]):
            # no more valid moves available for either player
            self.turn = -self.turn
            if not any([self.is_valid(i, j) for i in range(6) for j in range(6)]):
                return True
        return False
    
        
    def reset_game(self):
        #reset the game to its inital state
        self.board = [[0 for _ in range(6)] for _ in range(6)]
        self.board[2][2] = self.board[3][3] = 1
        self.board[2][3] = self.board[3][2] = -1
        return
    

    def count_flips(self, x, y):
        # count the potential flips if the next move is x, y
        flips = 0
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            i, j = x + dx, y + dy
            if i < 0 or i > 5 or j < 0 or j > 5:
                # out of bounds
                continue
            if self.board[i][j] == -self.turn:
                # opponent's piece found
                i, j = i + dx, j + dy
                while i >= 0 and i <= 5 and j >= 0 and j <= 5 and self.board[i][j] == -self.turn:
                    i, j = i + dx, j + dy
                if i >= 0 and i <= 5 and j >= 0 and j <= 5 and self.board[i][j] == self.turn:
                    # our piece found, flip pieces in between
                    i, j = x + dx, y + dy
                    while self.board[i][j] == -self.turn:
                        flips+=1
                        i, j = i + dx, j + dy
        return flips

    
    def is_on_board(self, x, y):
        return 0 <= x < 6 and 0 <= y < 6
    
    
    def get_canonical_board(self, board, player):
        #enable to change the board view for the current player
        return (np.asarray(board)*player).tolist()

    def translation_board_to_list(self,x, y):
        # from coordinate x, y, give the position if the boad is just a list
        return 6*x+y

    
    def translation_list_to_board(self,position):
        # from position in the list, give the position if the list is a board
        return (int(position/6), position%6) 

    
    def board_to_list(self, state_board):
        # from coordinate x, y, give the position if the boad is just a list
        liste_representation = []
        for liste in state_board:
            liste_representation += liste
        return liste_representation

    
    def symetry(self, state_board, pi):
        # give all symetries in order to increase the size of the dataset quickly
        symetry_list = []
        for i in range(1,5):
            new_borad = np.rot90(state_board, i)
            new_pi = np.rot90(pi, i)
            symetry_list.append((new_borad, new_pi))
        return symetry_list


