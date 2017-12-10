import logging
import numpy as np
import tensorflow as tf

from decision_engines.a3c_research import game_env as env
from decision_engines.a3c_research.a3c_model import ActorCriticNetwork


class TrainingNetwork(ActorCriticNetwork):
    def __init__(self, *args, **kwargs):
        self.model_path = kwargs.get("model_path")
        self.lr = kwargs.get("lr", 0.001)
        self.trainer = kwargs.get("trainer", tf.train.AdamOptimizer(learning_rate=self.lr))
        super().__init__(*args, **kwargs)

    def initialize_scope(self):
        super().initialize_scope()
        self.actions = tf.placeholder(shape=[None], dtype=tf.int32)
        self.one_hot_encoded_actions = tf.one_hot(self.actions, 7, dtype=tf.float32)
        self.target_value = tf.placeholder(shape=[None], dtype=tf.float32)
        self.advantages = tf.placeholder(shape=[None], dtype=tf.float32)
        self.actor_output = tf.squeeze(self.actor_output, axis=[0])

        self.action_played = tf.reduce_sum(self.one_hot_encoded_actions * self.actor_output[1])

        # Loss functions
        self.value_loss = 0.5 * tf.reduce_sum(tf.square(self.target_value - tf.reshape(self.critic_output, [-1])))
        self.entropy = - tf.reduce_sum(self.actor_output * tf.log(self.actor_output))
        self.policy_loss = -tf.reduce_sum(tf.log(self.action_played) * self.advantages)
        self.loss = 0.5 * self.value_loss + self.policy_loss - self.entropy * 0.01

        # update gradients
        self.trainer.minimize(self.loss)

    def work(self, max_episode_length, gamma, saver):
        episode_count = 0
        for i in range(max_episode_length):
            episode_buffer = []
            episode_frames = []
            episode_reward = 0
            episode_step_count = 0

            init_game_state = env.reset()
            episode_frames.append(init_game_state)
            lstm_c_state, lstm_h_state = self.input_c, self.input_h
            for stage in range(3000):
                # save the history of the game when the decision was made
                s_lstm_h_state, s_lstm_c_state = lstm_h_state, lstm_c_state

                # get an action distribution and estimate value from policy
                estimated_value, action_distribution, lstm_c_state, lstm_h_state = self.sess.run(
                    [self.critic_output, self.actor_output, self.c_state_out, self.h_state_out],
                    feed_dict={
                        self.inputs: init_game_state,
                        self.c_state_in: lstm_c_state,
                        self.h_state_in: lstm_h_state
                    })

                action_distribution = np.squeeze(action_distribution)

                # select action
                if init_game_state[0][-1] == 0:
                    legal_moves = np.nonzero(init_game_state[0][:7])
                else:
                    legal_moves = np.nonzero(init_game_state[0][8:15])
                legal_set = set(legal_moves[0])
                action_distribution = [prob if i in legal_set else 0 for i, prob in enumerate(action_distribution)]
                action_distribution /= sum(action_distribution)
                action = int(np.random.choice(np.arange(7), p=action_distribution))

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
                        estimated_value,
                        s_lstm_c_state,
                        s_lstm_h_state
                    ]
                )

                # add reward for episode + update state
                episode_reward += reward
                init_game_state = next_game_state
                episode_step_count += 1

                if game_over:
                    break

            # Update the network using the episode buffer at the end of the episode.
            if len(episode_buffer) != 0:  #
                value_loss, policy_loss, _ = self.update_params(episode_buffer, self.sess, gamma)
                logging.warning(
                    'For episode %s: we have value loss: %s '
                    'and policy loss: %s' % (episode_count, value_loss, policy_loss)
                )
                # pass

            # Periodically save gifs of episodes, model parameters, and summary statistics.
            if episode_count != 0:
                saver.save(self.sess, self.model_path + '/model-' + str(episode_count) + '.ckpt')
                print("Saved Model")
                # pass

            episode_count += 1

    @staticmethod
    def discount(ret, gamma):
        dis_ret = []
        # long term returns are worth more than short term
        for i, r in enumerate(reversed(ret)):
            dis_ret.append(r * (gamma ** i))

        # put the discounted returns back in chronological order
        return np.array([i for i in reversed(dis_ret)])

    def update_params(self, episode_buffer, sess, gamma):
        episode_buffer = np.array(episode_buffer)
        game_states = episode_buffer[:, 0]
        actions = episode_buffer[:, 1]
        rewards = episode_buffer[:, 2]
        values = episode_buffer[:, 5]
        c_states = episode_buffer[0, 6]
        h_states = episode_buffer[0, 7]
        values = np.append(values, values[-1])

        # Here we take the rewards and values from the episode_buffer, and use them to
        # generate the advantage and discounted returns.
        # The advantage function uses "Generalized Advantage Estimation"
        discounted_rewards = self.discount(rewards, gamma)
        advantages = rewards + gamma * values[1:] - values[:-1]
        advantages = np.squeeze(self.discount(advantages, gamma))

        value_loss, policy_loss, total_loss = sess.run([self.value_loss, self.policy_loss, self.loss], feed_dict={
            self.inputs: np.vstack(game_states),
            self.target_value: discounted_rewards,
            self.actions: actions,
            self.c_state_in: c_states,
            self.h_state_in: h_states,
            self.advantages: advantages
        })
        return value_loss, policy_loss, total_loss


if __name__ == '__main__':
    path_to_be_stored = "."
    max_episodes = 4
    gamma = 0.3
    workers = []
    master_network = TrainingNetwork(model_path=path_to_be_stored, state_size=17)
    with master_network.sess:
        saver = tf.train.Saver()
        master_network.work(max_episodes, gamma, saver)
