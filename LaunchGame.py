import random
import numpy as np
from tqdm import tqdm



from Othello import Othello
from MCTS import MonteCarloTreeSearch, Node
from IA_NeuralNetwork import nn_alpha_zero, neural_network_agent
from Players import MockModel_random,MockModel_greedy,HumanPlayer


# Enable to launch a game between two agents

class LaunchGame:
    def __init__(self, game, player1, player2):
        self.game = game
        self.player1 = player1
        self.player2 = player2
        return 

    def launchTwoPlayers(self, viz = 0):
        # Launch a game with the two players and give the winner
        self.game.reset_game()
        if viz != 0 :
            self.game.display()
        while not self.game.is_game_over():
            if viz != 0 :
                print("the current player is :",self.game.get_turn())

            if self.game.get_turn() == 1:
                x, y = self.player1.next_move(1)
            else :
                x, y = self.player2.next_move(-1)

            if not self.game.play(x, y):
                #if we can't play anything
                if len(self.game.valid_actions())==0:
                    self.game.turn = -1*self.game.turn
                else : 
                    print("error, not correct move")
                    return "Error, the game has been stoped due to not valid move"
            
            if viz != 0 :
                self.game.display()
          
        winner = self.game.get_winner()
        if viz != 0 :
                print("The winner is :", winner)
        return winner


    def launch_n_games(self, n_games = 200, viz = 0):
        # Launch n_games games and give the proportion of games win by player1
        victoire_joueur1 = 0
        print("launch n games")
        for i in tqdm(range(n_games)):
            self.game.reset_game()
            resultat = self.launchTwoPlayers()
            if resultat==1:
                victoire_joueur1+=1
        return victoire_joueur1/n_games
