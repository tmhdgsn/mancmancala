import java.util.ArrayList;

public interface DecisionEngine {
    static final int MANCALA = 7;

    public int getMove();

    public String hash(MancalaBoard board);

    public ArrayList<Integer> getLegalMoves(MancalaBoard board, Side side);

    public int intermediateScore(MancalaBoard board);

    public boolean gameOver(MancalaBoard board);

    public int gameScore(MancalaBoard board);

    public MancalaBoard getNextBoard(boolean agentHasMoved, Side side, MancalaBoard board, int move);

    public MancalaBoard playHole(int move, MancalaBoard boardCopy, Side agentSide);
}
