import java.util.Arrays;
import java.util.Collections;

public class MancalaBoard {
    public int [][] board;
    public int holes;
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
        this.board[0][this.holes] = 0;
        this.board[1][this.holes] = 0;
    }

    public MancalaBoard(MancalaBoard mancalaBoard) {
        this.board = mancalaBoard.board;
        this.holes = mancalaBoard.holes;
        this.seeds = mancalaBoard.seeds;
    }

    public MancalaBoard(int[][] board){
        this.board = board;
        this.holes = board[0].length - 1;
        this.seeds = 7;
    }

    public MancalaBoard copy() {
        return new MancalaBoard(this);
    }

    public int[] getLegalMoves(Side side) {
        //TODO improve god awful code
        int nonzeroPits = 0;
        for (int i = 0; i < this.holes + 1; i++) {
            if (this.board[side.value][i] != 0) {
                nonzeroPits++;
            }
        }
        int[] legalMoves = new int[nonzeroPits];
        for (int i = 0; i < this.holes + 1; i++) {
            if (this.board[side.value][i] != 0) {
                legalMoves[i] = i;
            }
        }
        return legalMoves;
    }

    public boolean gameOver() {
        boolean game_over = false;
        int north_score = 0;
        int south_score = 0;
        int[] north = this.board[Side.NORTH.value];
        int[] south = this.board[Side.SOUTH.value];
        for (int i = 0; i < this.holes; i++){
            north_score += north[i];
            south_score += south[i];
        }
        if (south_score == 0 || north_score == 0) {
            game_over = true;
        }
        return game_over;
    }

    public double[] getScore() {
        return new double[0];
    }

    public void updateBoardFromRawState(String raw_state) {
        String[] pit_values = raw_state.split(",");
        for (int i = 0; i <= this.holes; i++){
            this.board[Side.NORTH.value][i] = Integer.parseInt(pit_values[i]);
        }
        Collections.reverse(Arrays.asList(pit_values));
        for (int i = 0; i <= this.holes; i++) {
            this.board[Side.SOUTH.value][(this.holes - i)] = Integer.parseInt(pit_values[i]);
        }
    }

}
