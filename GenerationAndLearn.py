import random
import numpy as np
import random
import numpy as np
import copy


from Othello import Othello
from MCTS import MonteCarloTreeSearch, Node
from LaunchGame  import LaunchGame
from IA_NeuralNetwork import nn_alpha_zero, neural_network_agent
from Players import alpha_zero_agent, MockModel_random,MockModel_greedy,HumanPlayer
from tqdm import tqdm



# Create the dataset for the learning of the neural network and take care of all the learning part

class dataset_generation_and_learn:
    def __init__(self, game, nn_alpha_zero, num_sim):
        self.game = game
        self.nn_current = nn_alpha_zero
        self.num_sim = num_sim
        self.taille_max_dataset = 2000
        self.taille_partie = 60
        self.data_history = []
        self.mcts = MonteCarloTreeSearch(num_sim, self.nn_current, self.game)


    def learn(self):
        # Launch all the learning process, by creating the dataset, then check if the new agent is 
        # better than the previous one in order to save it or not
        data = self.create_dataset()
        new_nn = copy.deepcopy(self.nn_current)
        b, pis, v = list(zip(*data))
        b = np.asarray(b)
        pis = np.asarray(pis)
        v = np.asarray(v)
       
        new_nn.learning(b, pis, v)
        
        game = Othello() 
        MCTS_current_agent = MonteCarloTreeSearch(self.num_sim, self.nn_current, game)
        MCTS_new_agent = MonteCarloTreeSearch(self.num_sim, new_nn, game)
        
        current_agent = alpha_zero_agent(game, MCTS_current_agent)
        new_agent =  alpha_zero_agent(game, MCTS_new_agent)

        confrontation = LaunchGame(game, current_agent, new_agent)
        resultat = 1 - confrontation.launch_n_games(n_games =60, viz = 0)
        if resultat>0.57:
            self.nn_current = new_nn
            return True
        else :
            return False
    

    def save_model(self,compteur):
        # Save the neural network model in order to be used later
        name = "neural_network" + str(compteur)
        self.nn_current.nn.model.save(name)
        return 
    

    def create_dataset(self):
        # Create a dataset by launching games of the agent against itself
        print("Dataset creation")
        games_dataset = []
        for i in tqdm(range(self.taille_partie)):
            self.game.reset_game()
            self.mcts = MonteCarloTreeSearch(self.num_sim, self.nn_current, self.game)
            games_dataset += self.execute_game()
        
        self.data_history.append(games_dataset)
        #print(self.data_history[0][0])
        if len(self.data_history)>1:
            self.data_history = self.data_history[-2:]
            data_training = self.data_history[-1] + self.data_history[-2]
        else :
            data_training = self.data_history[-1]
        random.shuffle(data_training)
        
        return data_training

    def execute_game(self):
        # Launch a full game of the agent against itself. By knowing the outcome of the game, create a dataset. 
        # In order to extend it, we use the symetry of the game to to have more data
        self.game.reset_game()
        train_examples =[]
        board = copy.deepcopy(self.game.board)
        current_player = 1
        episode_count = 0
        while True:
            episode_count+=1
            
            canonical_board = self.game.get_canonical_board(board, current_player)
            
            pi = self.mcts.next_action_proba(board, current_player)
            sym = self.game.symetry(canonical_board, pi)
            for b, p in sym:
                train_examples.append([b, current_player, p, None])
            
            transform_pi = self.game.board_to_list(pi)

            transform_action = np.random.choice(len(transform_pi), p=transform_pi)

            action = self.game.translation_list_to_board(transform_action)

            self.game.turn = copy.deepcopy(current_player)
            self.game.board = copy.deepcopy(board)
            board = self.game.get_next_state(action)
            current_player *= -1
            reward = self.game.get_winner(1)
 
            if reward is not None:
                return [(x[0], x[2], reward * x[1]) for x in train_examples]

