import java.util.ArrayList;

public class MancalaBoard implements Board {
    private int [][] board;
    private int holes;
    private int seeds;

    public MancalaBoard(int holes, int seeds) {
        this.holes = holes;
        this.seeds = seeds;
        this.board = new int[2][holes + 1];
        for (int i = 0; i < this.board[0].length; i++){
            this.board[0][i] = this.seeds;
            this.board[1][i] = this.seeds;
        }
        // empty mancalas
        this.board[0][this.holes + 1] = 0;
        this.board[1][this.holes + 1] = 0;
    }

    public MancalaBoard(MancalaBoard mancalaBoard) {
        this.board = mancalaBoard.board;
        this.holes = mancalaBoard.holes;
        this.seeds = mancalaBoard.seeds;
    }

    @Override
    public Board copy() {
        return new MancalaBoard(this);
    }

    @Override
    public ArrayList<Move> getLegalMoves(CallLocation callLocation) {
        return null;
    }

    @Override
    public void playHole(Move m) {

    }

    @Override
    public boolean gameOver() {
        return false;
    }

    @Override
    public int getCurrentPlayer() {
        return 0;
    }

    @Override
    public int getQuantityOfPlayers() {
        return 0;
    }

    @Override
    public double[] getScore() {
        return new double[0];
    }

    @Override
    public double[] getMoveWeights() {
        return new double[0];
    }

    @Override
    public void bPrint() {

    }

    public void updateBoard(int i) {
    }
}
