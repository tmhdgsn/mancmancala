class BoundPlays {
    double ucb;
    int move;
    MancalaBoard board;

    public BoundPlays(double ucb, int move, MancalaBoard board) {
        this.ucb = ucb;
        this.move = move;
        this.board = board;
    }

    static int compare(BoundPlays b1, BoundPlays b2){
        return Double.compare(b1.ucb, b2.ucb);
    }
}
