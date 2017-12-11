import java.util.Objects;

class GameState {
    MancalaBoard board;
    int move;
    Side side;

    GameState(MancalaBoard board, int move, Side side) {
        this.board = board;
        this.move = move;
        this.side = side;
    }


    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        GameState gameState = (GameState) o;
        return move == gameState.move &&
                Objects.equals(board, gameState.board) &&
                side == gameState.side;
    }

    @Override
    public int hashCode() {

        return Objects.hash(board, move, side);
    }
}
