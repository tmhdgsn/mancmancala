public class MancalaMove implements Move {
    int pit;
    int side;

    public MancalaMove(int i, int side) {
        this.pit = i;
        this.side = side;
    }

    @Override
    public int compareTo(Move move) {
        return 0;
    }
}
