import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

public abstract class DecisionEngine {

    static final int MANCALA = 7;
    Agent agent;
    private HashMap<Integer, HashMap<Integer, ResultantBoard>> cache = new HashMap<>();

    public DecisionEngine(Agent agent) {
        this.agent = agent;
    }

    abstract int getMove();

    private int hash(MancalaBoard board) {
        return Arrays.deepToString(board.board).hashCode();
    }

    ArrayList<Integer> getLegalMoves(MancalaBoard board, Side side) {
        ArrayList<Integer> legalMoves = new ArrayList<>(board.holes);
        for (int i = 0; i < board.holes; i++) {
            if (board.board[side.value][i] != 0) {
                legalMoves.add(i);
            }
        }
        return legalMoves;
    }

    boolean gameOver(MancalaBoard board) {
        boolean game_over = false;
        int north_score = 0;
        int south_score = 0;
        int[] north = board.board[Side.NORTH.value];
        int[] south = board.board[Side.SOUTH.value];
        for (int i = 0; i < board.holes; i++){
            north_score += north[i];
            south_score += south[i];
        }
        if (south_score == 0 || north_score == 0) {
            game_over = true;
        }
        return game_over;
    }

    int gameScore(MancalaBoard board) {
        int opponent_score = 0;
        int my_score = 0;
        for (int i = 0; i < board.holes + 1; i++) {
            opponent_score += board.board[this.agent.side.opposite().value][i];
            my_score += board.board[this.agent.side.value][i];
        }
        return my_score - opponent_score;
    }

    private boolean playHole(int move, MancalaBoard boardCopy, Side agentSide) {
        int seeds = boardCopy.board[agentSide.value][move];
        boardCopy.board[agentSide.value][move] = 0;
        int cur_hole = (move + 1);
        Side currentSide = agentSide;
        while (seeds > 1) {
            if ((currentSide != agentSide) && (cur_hole == MANCALA)){
                cur_hole = (cur_hole + 1) % 8;
                currentSide = currentSide.opposite();
            }
            boardCopy.board[currentSide.value][cur_hole] += 1;
            if (cur_hole > 6) {
                currentSide = currentSide.opposite();
            }
            cur_hole = (cur_hole + 1) % 8;
            seeds -= 1;
        }

        int opposite_hole = MANCALA - 1 - move;
        // check if we can capture opponent pieces
        if ((cur_hole != MANCALA)
                && (currentSide == agentSide)
                && (boardCopy.board[currentSide.value][cur_hole] == 0
                && (boardCopy.board[currentSide.opposite().value][opposite_hole] > 0))) {
            int captured_seeds = boardCopy.board[currentSide.opposite().value][opposite_hole];
            boardCopy.board[currentSide.opposite().value][opposite_hole] = 0;
            boardCopy.board[currentSide.value][MANCALA] += captured_seeds;
            return false;
        }

        boardCopy.board[currentSide.value][cur_hole] += 1;
        return (currentSide == agentSide && cur_hole == MANCALA);
    }

    ResultantBoard getNextBoard(boolean agentHasMoved, Side side, MancalaBoard board, int move) {
        int board_hash = this.hash(board);
        if (!this.cache.containsKey(board_hash)){
            this.cache.put(board_hash, new HashMap<>());
        }
        if (this.cache.get(board_hash).containsKey(move)){
            MancalaBoard board_copy = board.copy();
            Boolean repeat = (this.playHole(move, board_copy, side) && (agentHasMoved || this.agent.side == Side.NORTH));
            ResultantBoard<MancalaBoard, Boolean> resultantBoard = new ResultantBoard<>(board_copy, repeat);
            this.cache.get(board_hash).put(move, resultantBoard);
            return resultantBoard;
        }
        return this.cache.get(board_hash).get(move);
    }


}
