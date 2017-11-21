from copy import deepcopy

from side import Side
from game import Game

my_side = Side.NORTH
MANKALAH = 7


def get_msg():
    from_engine = input().strip()
    output_(f"from engine: {from_engine}")
    args = from_engine.split(";")
    return args[0], args[1:]


def send_msg(msg):
    output_(f"from agent: {msg}")
    print(msg)


def output_(msg):
    with open("output.txt", "a") as f:
        f.write(msg + "\n")


def play_hole(hole, board_copy, agent_side):
    seeds = board_copy[agent_side.value][hole]
    board_copy[agent_side.value][hole] = 0
    cur_hole = (hole + 1)
    current_side = agent_side if cur_hole < 8 else agent_side.opposite()
    while seeds > 0:
        # only increment my mankalah
        if current_side != agent_side and cur_hole == MANKALAH:
            cur_hole = (cur_hole + 1) % 8
            current_side = current_side.opposite()
            continue
        board_copy[current_side.value][cur_hole] += 1
        if cur_hole > 6:
            current_side = current_side.opposite()
        cur_hole = (cur_hole + 1) % 8
        seeds -= 1

    return board_copy


def min_max(board, remaining_depth=3):
    # if the sum of all holes - mankalah is 0 game over
    if sum(board[my_side.opposite().value][:MANKALAH]) == 0:
        return -1, game_score(board, my_side.opposite())

    # shitty depth control to prevent death of CPU
    if remaining_depth == 0:
        return -1, intermediate_score(board, my_side)

    best_r = 1
    best_hole = -1
    for i, hole in enumerate(board[my_side.opposite().value][:MANKALAH]):
        # if Opponent can play then play
        if hole > 0:
            board_copy = deepcopy(board)
            play_hole(i, board_copy, my_side.opposite())
            # back to our go
            _, reward = max_min(board_copy, remaining_depth - 1)

            # minimize the reward
            if best_hole == -1 or reward > best_r:
                best_hole = i
                best_r = reward
    output_("MIN MOVE, %d" % (best_hole + 1))
    return best_hole, best_r


def intermediate_score(board, my_side):
    return board[my_side.value][MANKALAH] - board[my_side.opposite().value][MANKALAH]


def max_min(board, remaining_depth=3):
    # if the sum of all holes - mankalah is 0 game over
    if sum(board[my_side.value][:MANKALAH]) == 0:
        return -1, game_score(board, my_side)

    # shitty depth control to prevent death of CPU
    if remaining_depth == 0:
        return -1, intermediate_score(board, my_side)

    # else we traverse game tree
    best_r = -1
    best_hole = -1
    # for each hole on my side
    for i, hole in enumerate(board[my_side.value][:MANKALAH]):
        # if I can play that hole
        # play it and then let my opponent play
        if hole > 0:
            board_copy = deepcopy(board)
            play_hole(i, board_copy, my_side)
            _, reward = min_max(board_copy, remaining_depth - 1)
            # maximize the reward
            if best_hole == -1 or reward > best_r:
                best_hole = i
                best_r = reward
    output_("MAX MOVE, %d" % (best_hole + 1))

    return best_hole, best_r


def game_score(board, side):
    opponent_score = sum(board[side.opposite().value])
    my_score = board[side.value][MANKALAH]
    return my_score - opponent_score


def make_move(game):
    move, reward = max_min(game.board, 4)
    return move + 1


if __name__ == '__main__':
    our_turn = False
    holes = 7
    seeds = 7
    game = Game()
    while True:
        msg_type, args = get_msg()
        if msg_type.upper() == "START":
            if args[0].upper() == "SOUTH":
                my_side = Side.SOUTH
                our_turn = True
            else:
                my_side = Side.NORTH
        if msg_type.upper() == "END":
            break
        if msg_type.upper() == "CHANGE":
            our_turn = args[-1].upper() == "YOU"
            game.update_board(args[-2])
            if args[1].upper() == "SWAP":
                my_side = my_side.opposite()
            output_(repr(game))
        if our_turn:
            move = make_move(game)
            send_msg(f"MOVE;{move}")
