# Script to calculate reward

REWARD_PROBS = dict()


def calculate_reward(previous_line, our_side, probs):
    split_previous_lines = previous_line.split(' ')
    command = split_previous_lines[0].split(';')[2]
    board = list(map(int, command.split(',')))
    reward = board[7] - board[15] if our_side == 'NORTH' else board[15] - board[7]
    REWARD_PROBS[tuple(probs)] = reward

    
def calculate_max():
    return max(zip(REWARD_PROBS.values(), REWARD_PROBS.keys()))


if __name__ == '__main__':
    f = open('./output.txt')
    our_side = 'NORTH'
    all_lines = f.readlines()
    previous_line = ''

    for i in range(len(all_lines)):
        split_it_on_spaces = all_lines[i].strip('\n').split(' ')
        command, probabilities = split_it_on_spaces[0], split_it_on_spaces[1:]
        if command.startswith('START'):
            our_side = command.split(';')[1]

        if command.startswith('CHANGE') and command.split(';')[1] == 'SWAP':
            our_side = 'SOUTH' if our_side == 'NORTH' else 'NORTH'
            
        if command.startswith('END'):
            calculate_reward(all_lines[i - 1], our_side, probabilities)

    print(calculate_max())
