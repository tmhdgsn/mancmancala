import os
import numpy as np
import tensorflow as tf


class ActorCriticNetwork:
    def __init__(self, *args, **kwargs):
        self.graph = tf.Graph()

        # parse all the keyword args into the instance variables
        self.num_outputs = kwargs.get("encoded_board_size", 400)
        self.num_of_actions = kwargs.get("num_of_actions", 7)
        self.lstm_layers = kwargs.get("lstm_layers", 1)
        self.lstm_size = kwargs.get("lstm_size", 512)
        self.inputs = kwargs.get("inputs")
        self.critic_output = kwargs.get("critic_output")
        self.actor_output = kwargs.get("actor_output")
        self.init_graph = kwargs.get("init_graph")
        self.state_size = kwargs.get("state_size", 17)
        self.model_name = kwargs.get("param_file", "best-weights")
        # self.state = None# Will be set implicitly by tensorflow
        self.input_c = np.zeros((1, self.lstm_size), np.float32)
        self.input_h = np.zeros((1, self.lstm_size), np.float32)
        self.sess = kwargs.get("sess", tf.Session(graph=self.graph))


        # initialize the computational graph
        with self.graph.as_default():
            self.initialize_scope()
            model_path = os.path.expanduser('~/' + self.model_name)
            if self.model_name and os.path.isfile(model_path + '.ckpt.meta'):
                saver = tf.train.Saver()
                saver.restore(self.sess, model_path + '.ckpt')
            else:
                self.init_graph = tf.global_variables_initializer()
                self.sess.run(self.init_graph)

    def initialize_scope(self):

        # Encode inputs with NN
        self.inputs = tf.placeholder(tf.float32, [None, self.state_size], name='inputs')
        encoded_inputs = tf.contrib.layers.fully_connected(self.inputs, self.num_outputs)

        # Expand dimensions so that LSTM can process
        rnn_inputs = tf.expand_dims(encoded_inputs, [0])

        # Model the game through time
        lstm = tf.contrib.rnn.BasicLSTMCell(self.lstm_size)
        self.c_state_in = tf.placeholder(dtype=tf.float32, shape=[1, lstm.state_size.c])
        self.h_state_in = tf.placeholder(dtype=tf.float32, shape=[1, lstm.state_size.h])
        state = tf.contrib.rnn.LSTMStateTuple(self.c_state_in, self.h_state_in)

        # Get output of game model
        outputs, state = tf.nn.dynamic_rnn(
            lstm, rnn_inputs, dtype=tf.float32, initial_state=state
        )

        # read out what the new state is
        self.c_state_out, self.h_state_out = state

        # calculate the value of move
        self.critic_output = tf.contrib.layers.fully_connected(
            outputs, 1, activation_fn=None
        )

        # calculate the distribution of actions
        self.actor_output = tf.contrib.layers.fully_connected(
            outputs, self.num_of_actions, activation_fn=tf.nn.softmax
        )

    def __call__(self, game_board, *args, **kwargs) -> np.array:
        critic_output, actor_output, self.input_c, self.input_h = self.sess.run(
            [self.critic_output, self.actor_output, self.c_state_out, self.h_state_out],
            feed_dict={
                self.inputs: game_board,
                self.c_state_in: self.input_c,
                self.h_state_in: self.input_h
            })

        return critic_output, actor_output

    def exit(self):
        """
        Closes session if open,
        tensorflow already has a isOpen check
        :return:
        """
        self.sess.close()
