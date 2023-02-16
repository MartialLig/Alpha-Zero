import random
import numpy as np
import random
import numpy as np
import copy

from Othello import Othello
from MCTS import MonteCarloTreeSearch, Node
from IA_NeuralNetwork import nn_alpha_zero, neural_network_agent


# This file contains all kind of  players :
# alpha_zero_agent : Alpha Zero player
# MockModel_random : a player playing randomly
# MockModel_greedy : a greedy player choosing to maximize at each step the number of coins it flips
# HumanPlayer : a player which follow your order


##########################################################################################################################################################


# Alpha Zero player
class alpha_zero_agent:
    def __init__(self, game, MCTS):
        self.game = game
        self.MCTS = MCTS
    
    
    def next_move(self, player):
        # Choose the next move to do by using the polocy of alpha zero
        probs = self.MCTS.next_action_proba(copy.deepcopy(self.game.board), player)
        probs = np.asarray(probs)
        max_position = probs.argmax()
        x,y = self.game.translation_list_to_board(max_position)
        return x, y
 

##########################################################################################################################################################

# Random player class
class MockModel_random:
    def __init__(self, game):
          self.game = game


    def predict(self, state):
        # Give a random prior_prediction_board and policy (in order to test the MCTS)
        prior_prediction  = self.game.valid_actions()
        prior_prediction_board = [[0 for _ in range(6)] for _ in range(6)]
        random_priors = [random.random() for x in range(len(prior_prediction))]
        total = np.sum(random_priors)
        random_priors = [x/total for x in random_priors]
        count = 0
        for x, y in prior_prediction :
            prior_prediction_board[x][y] = random_priors[count]
            count +=1
        policy = 0.001
        return prior_prediction_board, policy


    def next_move(self,player):
        # Choose randomly the next move to do 
        liste = self.game.valid_actions()
        number = random.randint(0, len(liste)-1)
        x, y = liste[number]
        return x, y
    
##########################################################################################################################################################

# Classe d'un joueur greedy
class MockModel_greedy:
    def __init__(self, game):
          self.game = game
    

    def predict(self, state):
        # Give a random prior_prediction_board and policy (in order to test the MCTS)
        prior_prediction  = self.game.valid_actions()
        prior_prediction_board = [[0 for _ in range(6)] for _ in range(6)]
        random_priors = [random.random() for x in range(len(prior_prediction))]
        total = np.sum(random_priors)
        random_priors = [x/total for x in random_priors]
        count = 0
        for x, y in prior_prediction :
            prior_prediction_board[x][y] = random_priors[count]
            count +=1
        policy = 0.001
        return prior_prediction_board, policy


    def next_move(self, player):
        # Iterates over all possible moves and selects the move with maximum number of pieces being flipped
        best_move = None
        max_flips = 0
        for x in range(6):
            for y in range(6):
                if self.game.is_valid(x, y):
                    flips = self.game.count_flips(x, y)
                    if flips > max_flips:
                        max_flips = flips
                        best_move = (x, y)
        return best_move[0], best_move[1]

##########################################################################################################################################################

class HumanPlayer:
    def __init__(self, game):
          self.game = game

    def next_move(self,player):
        # enable a human to play the game
        while True:
            #print(self.game.valid_actions_mask())
            x, y = input("Enter your move (row col): ").split()
            x, y = int(x), int(y)
            if self.game.is_valid(x, y):
                break
            else:
                print("Invalid move, try again")
        return x, y
