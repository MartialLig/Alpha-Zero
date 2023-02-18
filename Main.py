import numpy as np


from Othello import Othello
from MCTS import MonteCarloTreeSearch, Node
from LaunchGame  import LaunchGame
from IA_NeuralNetwork import nn_alpha_zero, neural_network_agent
from Players import alpha_zero_agent, MockModel_random,MockModel_greedy,HumanPlayer
from GenerationAndLearn import dataset_generation_and_learn
from keras.models import load_model



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
    



def launch_learning_from_begining():
    #launch learning from begining,  neural networks are saved in the file
    launch = main() 
    launch.launch_training()
    return


#To launch learning, uncomment the line :
#launch_learning_from_begining()
def launch_a_game_to_play(model_number):
    #1 is human
    #2 is greedy model
    #3 is random model
    path = "neural_network15"
    nn = load_model(path)
    nn2 = neural_network_agent()
    nn2.model = nn
    nn_alpha = nn_alpha_zero( nn2, epochs = 10, batch_size = 64)

    game = Othello()

    MCTS_new_agent = MonteCarloTreeSearch(5, nn_alpha, game)
            
    new_agent =  alpha_zero_agent(game, MCTS_new_agent)

    player1 = new_agent# MockModel_greedy(game)
    if model_number == 2 :
        print("greedy model")
        player2 = MockModel_greedy(game) 
    elif model_number == 3 :
        player2 = MockModel_random(game)
        print("random model")
    else :
        player2 = HumanPlayer(game) 

    launcher = LaunchGame(game, new_agent, player2)
    launcher.launchTwoPlayers(1)
    print("alpha zero is player 1")
    return

#To launch a game of alpha zero against another agent (human, greedy or random), uncomment the line :
launch_a_game_to_play(3)
        



   