import numpy as np
from keras.models import Sequential
from keras.layers import Input,Flatten, BatchNormalization, Activation, LeakyReLU, add, Dense, Conv2D
from tensorflow.keras.optimizers import SGD, Adam
from keras import regularizers
from keras.layers import Reshape
from keras.models import Model
from keras.utils.vis_utils import plot_model
from keras.layers import Dropout




# Deal with the neural network
class nn_alpha_zero:
    def __init__(self, nn, epochs = 10, batch_size = 64):
        self.nn = nn
        self.batch_size = batch_size
        self.epochs = epochs
        return
      

    def predict(self,x):
        # give pi and value from a state x
        x = np.asarray(x).reshape(1,6,6)
        return self.nn.model.predict(x, verbose =False)


    def learning(self, b, pi, v):
        # Launch the learning of the neural network
        self.nn.model.fit(x = b, 
                          y = [pi, v], 
                          batch_size = self.batch_size, 
                          epochs =self.epochs)
        return


    def save_model(self):
        # Save the model
        self.nn.model.save()
        return

##########################################################################################################################################################


# Contain the architecture of our Keras Model
class neural_network_agent:

    def __init__(self, dropout_rate = 0.3, channels_cnn = 512, learning_rate = 0.001):
        self.dropout_rate = dropout_rate
        self.channels_cnn = channels_cnn
        self.learning_rate = learning_rate



        input_boards = Input(shape=(6, 6,))    

        new_input_boards = Reshape((6, 6, 1))(input_boards) 
        
        layer1 = Conv2D(self.channels_cnn, 3, padding='same', use_bias=False)(new_input_boards)
        layer1 = BatchNormalization(axis=3)(layer1)
        layer1 = Activation('relu')(layer1)

        layer2 = Conv2D(self.channels_cnn, 3, padding='same', use_bias=False)(layer1)
        layer2 = BatchNormalization(axis=3)(layer2)
        layer2 = Activation('relu')(layer2)

        layer3 = Conv2D(self.channels_cnn, 3, padding='valid', use_bias=False)(layer2)
        layer3 = BatchNormalization(axis=3)(layer3)
        layer3 = Activation('relu')(layer3)

        layer4 = Conv2D(self.channels_cnn, 3, padding='valid', use_bias=False)(layer3)
        layer4 = BatchNormalization(axis=3)(layer4)
        layer4 = Activation('relu')(layer4)

        layer4_flat = Flatten()(layer4)
        fc_layer1 = Dense(1024, use_bias=False)(layer4_flat)
        fc_layer1 = BatchNormalization(axis=1)(fc_layer1)
        fc_layer1 = Activation('relu')(fc_layer1)
        fc_layer1 = Dropout(self.dropout_rate)(fc_layer1)

        fc_layer2 = Dense(512, use_bias=False)(fc_layer1)
        fc_layer2 = BatchNormalization(axis=1)(fc_layer2)
        fc_layer2 = Activation('relu')(fc_layer2)
        fc_layer2 = Dropout(self.dropout_rate)(fc_layer2)

        pi = Dense(36, activation='softmax', name='pi')(fc_layer2)
        pi = Reshape((6,6))(pi)
        v = Dense(1, activation='tanh', name='v')(fc_layer2)

        model = Model(inputs=input_boards, outputs=[pi, v])
        model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=Adam(0.01))
        self.model = model
        return 

    def plot_model(self):
        return plot_model(self.model, show_shapes=True, show_layer_names=True)