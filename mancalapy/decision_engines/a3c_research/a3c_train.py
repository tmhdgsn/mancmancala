import logging
import numpy as np
import tensorflow as tf

from decision_engines.a3c_research import game_env as env
from decision_engines.a3c_research.a3c_model import ActorCriticNetwork


# Copies one set of variables to another.
# Used to set worker network parameters to those of global network.
def update_target_graph(from_scope, to_scope):
    from_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, from_scope)
    to_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, to_scope)

    op_holder = []
    for from_var, to_var in zip(from_vars, to_vars):
        op_holder.append(to_var.assign(from_var))
    return op_holder


class Worker(ActorCriticNetwork):
    def __init__(self, *args, **kwargs):
        self.model_path = kwargs.get("model_path")
        self.lr = kwargs.get("lr", 0.001)
        self.trainer = kwargs.get("trainer", tf.train.AdamOptimizer(learning_rate=self.lr))
        super().__init__(*args, **kwargs)
        self.sess = kwargs.get("sess")

    def initialize_scope(self, graph):
        super().initialize_scope(graph)
        # sync with global model
        self.update_local_ops = update_target_graph('global', self.scope_name)

        self.actions = tf.placeholder(dtype=tf.int32)
        self.total_reward = tf.placeholder(dtype=tf.float32)
        self.generalized_advantage = tf.placeholder(dtype=tf.float32)
        self.advantage = self.total_reward - tf.reshape(self.critic_output, [-1])

        # Loss functions
        self.value_loss += 0.5 * tf.reduce_sum(tf.square(self.advantage))
        self.entropy = -tf.reduce_sum(self.actor_output * tf.log(self.actor_output))
        self.policy_loss -= tf.reduce_sum(tf.log(self.actor_output) * self.generalized_advantage)
        self.loss = 0.5 * self.value_loss + self.policy_loss - self.entropy * 0.01

        # Get gradients from local network using local losses
        local_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, self.scope_name)
        self.gradients = tf.gradients(self.loss, local_vars)
        self.var_norms = tf.global_norm(local_vars)
        grads, self.grad_norms = tf.clip_by_global_norm(self.gradients, 40.0)

        # Apply local gradients to global network
        global_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'global')
        self.apply_grads = self.trainer.apply_gradients(zip(grads, global_vars))

    def work(self, max_episode_length, gamma, saver):
        total_steps = 0
        sess = self.sess
        with sess.as_default(), sess.graph.as_default():
            episode_count = 0
            for i in range(max_episode_length):
                # copy the local params from the global network
                sess.run(self.update_local_ops)
                episode_buffer = []
                episode_frames = []
                episode_reward = 0
                episode_step_count = 0
                game_over = False

                init_game_state = env.reset()
                episode_frames.append(init_game_state)
                lstm_c_state, lstm_h_state = self.c_init, self.h_init
                for i in range(30):
                    while not game_over:
                        # get an action distribution and estimate value from policy
                        action_distribution, estimated_value, lstm_c_state, lstm_h_state = sess.run([
                            self.actor_output, self.critic_output, self.c_state, self.h_state],
                            feed_dict={
                                self.inputs: init_game_state,
                                self.dropout_prob: 0.2,
                                self.c_state: lstm_c_state,
                                self.h_state: lstm_h_state
                            }
                        )

                        # select action
                        action = int(np.argmax(action_distribution))

                        # play action on game
                        next_game_state, reward, game_over = env.step(init_game_state, action)

                        # save game transition and estimated value
                        episode_buffer.append(
                            [
                                init_game_state,
                                action,
                                reward,
                                next_game_state,
                                game_over,
                                estimated_value
                            ]
                        )

                        # add reward for episode + update state
                        episode_reward += reward
                        init_game_state = next_game_state
                        total_steps += 1
                        episode_step_count += 1

                    # If the episode hasn't ended, but the experience buffer is full, then we
                    # make an update step using that experience rollout.
                if len(episode_buffer) == 30 and not game_over and episode_step_count != max_episode_length - 1:
                    self.update_params(episode_buffer, sess, gamma)
                    episode_buffer = []
                    sess.run(self.update_local_ops)

                # Update the network using the episode buffer at the end of the episode.
                if len(episode_buffer) != 0:
                    value_loss, policy_loss, entropy_loss, gradients, variance = self.update_params(episode_buffer,
                                                                                                    sess, gamma)
                    logging.warning(
                        'For episode %s: we have value loss: %s '
                        'and policy loss: %s' % (episode_count, value_loss, policy_loss)
                    )

                # Periodically save gifs of episodes, model parameters, and summary statistics.
                if episode_count != 0:
                    saver.save(sess, self.model_path + '/model-' + str(episode_count) + '.ckpt')
                    print("Saved Model")

                episode_count += 1

    def update_params(self, episode_buffer, sess, gamma):
        total_reward = 0
        total_generalized_advantage = 0
        for i, episode in enumerate(reversed(episode_buffer[:-1])):
            state, action, reward, value = episode[0], episode[1], episode[2], episode[5]
            next_value = episode_buffer[i + 1][5]
            total_reward = total_reward * gamma + reward
            advantage = total_reward - value
            delta_t = reward + gamma * next_value - value
            total_generalized_advantage = total_generalized_advantage * gamma + delta_t

            value_loss, policy_loss, entropy_loss, gradients, variance = sess.run([
                self.value_loss, self.policy_loss, self.loss, self.gradients, self.var_norms], feed_dict={
                self.inputs: state,
                self.dropout_prob: 0.2,
                self.actions: action,
                self.advantage: advantage,
                self.total_reward: total_reward,
                self.generalized_advantage: total_generalized_advantage
            })
        return value_loss, policy_loss, entropy_loss, gradients, variance


if __name__ == '__main__':
    path_to_be_stored = "."
    max_episodes = 2
    gamma = 0.3
    workers = []
    master_network = ActorCriticNetwork()
    with tf.Session() as sess:
        saver = tf.train.Saver()
        worker = Worker(0, scope_name=f"worker_0", state_size=17, saver=saver,
                        sess=master_network.sess, model_path=path_to_be_stored)
        worker.work(max_episodes, gamma=gamma, saver=saver)
