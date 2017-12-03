import tensorflow as tf

from decision_engines.a3c_research import game_env


class ActorCriticNetwork:
    def __init__(self, param_names="best_weights"):
        self.encoder = tf.contrib.fully_connected()
        # self.game_state = tf.LSTM...
        # self.policy_func =...
        # self.val_func =...

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
