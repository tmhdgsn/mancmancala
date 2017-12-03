import tensorflow as tf

import numpy as np


class ActorCriticNetwork:
    def __init__(self, num_of_actions=7, encoded_board_size=400, lstm_layers=1, lstm_size=512, param_file=None):
        self.graph = tf.Graph()

        self.num_outputs = encoded_board_size
        self.num_of_actions = num_of_actions  # Get the probability just for our side of the board
        self.state = None
        self.lstm_layers = lstm_layers
        self.lstm_size = lstm_size
        self.initialize_graph(self.graph)
        self.sess = tf.Session(graph=self.graph)
        self.sess.run(self.init_graph)
        # if we have weights
        # load weights
        # if param_file:
        #     saver = tf.train.Saver()
        #     saver.restore(self.sess, param_file)

    def initialize_graph(self, graph):
        with graph.as_default():
            # Probability for dropout
            self.inputs = tf.placeholder(tf.float32, [None, 17],
                                         name='inputs')  # Dimensions of this will be 1 x 17 for each of the states
            self.dropout_prob = tf.placeholder(tf.float32, name='keep_prob')

            # Let the activation function be RELu, we can play with it later on
            # Automatically creates weights with the help of the Xavier Initializer
            # https://www.tensorflow.org/api_docs/python/tf/contrib/layers/fully_connected
            encoded_inputs = tf.contrib.layers.fully_connected(self.inputs, self.num_outputs)
            rnn_inputs = tf.reshape(encoded_inputs, (1, 400, 1))
            # Forming an LSTM Layer
            lstm = tf.contrib.rnn.BasicLSTMCell(self.lstm_size)
            drop = tf.contrib.rnn.DropoutWrapper(lstm, output_keep_prob=self.dropout_prob)
            cell = tf.contrib.rnn.MultiRNNCell([drop] * self.lstm_layers)
            self.state = cell.zero_state(1, tf.float32)  # self.state if self.state else

            # Get the outputs and the final_state, which need to be fed in the Value and Policy network
            # final state comprises of c and h
            outputs, state = tf.nn.dynamic_rnn(
                cell, rnn_inputs, initial_state=self.state
            )

            self.critic_output = tf.contrib.layers.fully_connected(
                outputs, 1, activation_fn=None
            )
            self.actor_output = tf.contrib.layers.fully_connected(
                outputs, self.num_of_actions, activation_fn=tf.nn.softmax
            )
            self.init_graph = tf.global_variables_initializer()

    def __call__(self, game_board, *args, **kwargs) -> np.array:
        feed = {
            self.inputs: game_board,
            self.dropout_prob: kwargs.get("dropout_prob", 0.2),
        }
        critic_output, actor_output = self.sess.run([self.critic_output, self.actor_output], feed_dict=feed)

        return critic_output, actor_output

    def exit(self):
        """
        Closes session if open,
        tensorflow already has a isOpen check
        :return:
        """
        self.sess.close()
