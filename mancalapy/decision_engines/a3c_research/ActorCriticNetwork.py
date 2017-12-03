import tensorflow as tf

from decision_engines.a3c_research import game_env


class ActorCriticNetwork:
    def __init__(self, param_names="best_weights"):
        lstm_size = 512
        lstm_layers = 1  # Could be changed later on with the size
        learning_rate = 0.001
        num_outputs = 400

        # Probability for dropout
        self.inputs = tf.placeholder(tf.int32, [None, None],name='inputs')  # Dimensions of this will be 1 x 17 for each of the states
        self.dropout_prob = tf.placeholder(tf.float32, name='keep_prob')

        # Let the activation function be RELu, we can play with it later on
        # Automatically creates weights with the help of the Xavier Initializer
        # https://www.tensorflow.org/api_docs/python/tf/contrib/layers/fully_connected
        self.encoded_inputs = tf.contrib.layers.fully_connected(self.inputs, num_outputs)

        # Forming an LSTM Layer
        self.lstm = tf.contrib.rnn.BasicLSTMCell(lstm_size)
        self.drop = tf.contrib.rnn.DropoutWrapper(self.lstm, output_keep_prob=self.dropout_prob)
        self.cell = tf.contrib.rnn.MultiRNNCell([self.drop] * lstm_layers)
        self.initial_state = self.cell.zero_state(num_outputs, tf.float32)

        # Get the outputs and the final_state, which need to be fed in the Value and Policy network
        # final state comprises of c and h
        self.outputs, final_state = tf.nn.dynamic_rnn(self.cell, self.encoded_inputs, initial_state=self.initial_state)

        self.num_actor_outputs = 7  # Since we need the probability of the full board
        self.critic_output = tf.contrib.layers.fully_connected(self.outputs, 1, activation_fn=None)
        self.actor_output = tf.contrib.layers.fully_connected(
            self.outputs, self.num_actor_outputs, activation_fn=tf.nn.softmax
        )

    def __call__(self, *args, **kwargs) -> int:
        action = -1
        with tf.Session() as sess:
            # take the input state from the args
            # feed it into model
            # get back an action
            pass

            logits = 1  # dummy of all actions
            tf.nn.softmax(logits)

        return action

    def fit(self, nbepochs=50, steps=30, is_global=False,):
        for epoch in range(nbepochs):
            # sync local params with global model
            # initialize LSTM cell / H(output)

            values = []
            rewards = []
            log_prob = []
            entropies = []
            state = game_env.reset()
            for step in range(steps):
                # state =
                pass
