import numpy as np


from Othello import Othello
from MCTS import MonteCarloTreeSearch, Node
from LaunchGame  import LaunchGame
from IA_NeuralNetwork import nn_alpha_zero, neural_network_agent
from Players import alpha_zero_agent, MockModel_random,MockModel_greedy,HumanPlayer
from GenerationAndLearn import dataset_generation_and_learn




class main: 
    def __init__(self):
        self.nombre_model = 0
        self.performance_vs_random = []
        self.performance_vs_greedy = []
        self.jeu =  Othello()
        self.nn = neural_network_agent()
        self.IAplayer = nn_alpha_zero(self.nn)
        self.num_sim = 40
        self.learning = dataset_generation_and_learn(self.jeu, self.IAplayer, self.num_sim)
        return


    def launch_training(self):
        
        compteur = 0
        while compteur<20:
            print("Attempt #", compteur)
            if self.learning.learn():
                compteur+=1
                self.learning.save_model(compteur)
            else:
                print()
                print("Failure of learning")
                print()
        return 
    


launch = main() 
launch.launch_training()



   