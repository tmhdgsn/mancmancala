from side import Side
from game import Game

side = Side.NORTH


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


def make_move(board):
    my_side = board.board[side.value]
    for i in range(len(my_side) - 2, -1, -1):
        if my_side[i] > 0:
            return i + 1


if __name__ == '__main__':
    our_turn = False
    holes = 7
    seeds = 7
    game = Game()
    while True:
        msg_type, args = get_msg()
        if msg_type.upper() == "START":
            if args[0].upper() == "SOUTH":
                side = Side.SOUTH
                our_turn = True
            else:
                side = Side.NORTH
        if msg_type.upper() == "END":
            break
        if msg_type.upper() == "CHANGE":
            our_turn = args[-1].upper() == "YOU"
            game.update_board(args[-2])
            if args[1].upper() == "SWAP":
                side.opposite()
            output_(repr(game))
        if our_turn:
            move = make_move(game)
            send_msg(f"MOVE;{move}")
