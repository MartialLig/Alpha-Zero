
import numpy as np
import copy


from Othello import Othello


# Class for our Monte Carlo Tree Search

class MonteCarloTreeSearch :
    def __init__(self, num_sim, model, game):
        self.num_sim = num_sim
        self.model = model
        self.game = game
        self.nodes_dict = {}


    def next_action_proba(self, state, to_play):
        # Give a board with the probablity to do the next moves
        prob_list = [[0 for _ in range(6)] for _ in range(6)]
        root = self.run(state, to_play)
        children = root.children
        for child in children:
            prob_list[child[0]][child[1]] = children[child].visit_count

        total = np.sum(prob_list)
        prob_list = np.asarray(prob_list)/total
        self.game.board = state    
        self.game.turn = to_play    
        return prob_list.tolist()


    def run(self, state, to_play) :
        # From a board, launch the process of MCTS
        self.game.board = self.game.get_canonical_board(state, player=to_play)
        self.game.turn =  1
        if self.getKey(self.game.board) in self.nodes_dict :
            root = self.nodes_dict[self.getKey(self.game.board)]
        else :
            root = Node(0, to_play)
            action_probs, value = self.model.predict(self.game.board)
            action_probs = np.asarray(action_probs).reshape((6,6))
            valid_moves = self.game.valid_actions_mask()
            action_probs = np.asarray(action_probs) * np.asarray(valid_moves)  
            sum_action_probs = np.sum(action_probs) 
            action_probs = (np.asarray(action_probs)/sum_action_probs).tolist()
            root.expand(self.game.board, to_play, action_probs)
            self.nodes_dict[self.getKey(self.game.board)]=root
        count = 0 

        for _ in range(self.num_sim):
            node = root
            search_path = [node]
            while node.have_child():
                action, node = node.children_selection()
                search_path.append(node)
            
            parent = search_path[-2]
            state = parent.state
            self.game.board = copy.deepcopy(state)
            self.game.turn = 1

            next_state = self.game.get_next_state(action=action)
            next_state_other_view = self.game.get_canonical_board(next_state, player=-1)
            self.game.board = next_state_other_view
            self.game.turn = 1
            value = self.game.get_winner( player=1) 
            
            if value is None:
                # If the game has not ended:EXPAND
                action_probs, value = self.model.predict(self.game.board)
                action_probs = np.asarray(action_probs).reshape((6,6))
                valid_moves = self.game.valid_actions_mask()
                action_probs = np.asarray(action_probs) * np.asarray(valid_moves)  # mask invalid moves
                sum_action_probs = np.sum(action_probs) 
                action_probs = (np.asarray(action_probs)/sum_action_probs).tolist()


                node.expand(self.game.board, parent.to_play * -1, action_probs)
                self.nodes_dict[self.getKey(self.game.board)] = node

            self.backpropagation_path(search_path, parent.to_play * -1, value)
            count += 1
            
        return root

    
    def backpropagation_path(self, path, to_play, value_ending):
        # Enable to adjust the value of each node by knowing the outcome of a game
        for pastNode in path :
            pastNode.visit_count +=1
            if pastNode.to_play == to_play :
                pastNode.value_sum += value_ending
            else : 
                pastNode.value_sum += -value_ending
        return


    def getKey(self, state):
        # Give a unqiue id to each node in order to find it easily by its state
        matrix = np.array(state)
        flat_array = matrix.flatten()
        string = ','.join(map(str, flat_array))
        return string


    def from_key_to_matrix(self,string):
        # With a key, give back the state
        values = list(map(int, string.split(',')))
        matrix = np.array(values).reshape((6, 6))
        return matrix.tolist()
    

##########################################################################################################################################################################################################################



def UCB_values(parent_node, child_node):
    # Give a score which drive if we should to visit the child node or not
    prior_score = child_node.prior * (parent_node.visit_count)**0.5 / (child_node.visit_count + 1)
    if child_node.visit_count > 0:
        value_score = -child_node.value()
    else:
        value_score = 0
    return value_score + prior_score


##########################################################################################################################################################################################################################

# Node contains a state, a prior, the current player, a visit count, value sum and its children
class Node :
    def __init__(self, prior, to_play):
        self.visit_count = 0
        self.to_play = to_play
        self.prior = prior
        self.value_sum = 0
        self.children = {}
        self.state = None
        

    def have_child(self):
        # Check if the node has at least one child
        return len(self.children)>0


    def value(self):
        # Give the value
        if self.visit_count == 0:
            return 0 
        return self.value_sum / self.visit_count
        
    
    def children_selection(self):
        # Give the next child to explore
        UCB_max = -np.inf
        best_action = -1 
        child_min = None 
        for action, child in self.children.items():
            new_UCB = UCB_values(self, child)
            if new_UCB>UCB_max:
                UCB_max = new_UCB
                child_min = child 
                best_action = action
        return best_action, child_min
    

    def expand(self, state, to_play, action_probs):
        # Expand the node with its children 
        self.to_play = to_play
        self.state =  copy.deepcopy( state)
        for i in range(len(action_probs)):
            for j in range(len(action_probs[i])):
                prob = action_probs[i][j]
                if prob != 0:
                    self.children[(i,j)] = Node(prior=prob, to_play=self.to_play * -1)
        return




