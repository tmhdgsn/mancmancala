import java.util.ArrayList;

public interface Board {

    /**
     * copy the board
     * @return a copy of the board.
     */
    public Board copy();

    /**
     * Get a list of legal moves given the current state.
     * MCTS will call this to know what moves it can make.
     *
     * Call location can be either treePolicy or playout.
     *
     * @param callLocation from where in the algo getLegalMoves was called.
     * @return list of legal moves
     */
    public ArrayList<Move> getLegalMoves(CallLocation callLocation);

    /**
     * Apply the move m to the current state of the board.
     *
     * @param m
     */
    public void playHole(Move m);

    /**
     * if game is over return true
     *
     * @return if game is over
     */
    public boolean gameOver();

    /**
     * Returns the player ID for the player whose turn is active. This method is
     * called by the MCTS.
     *
     * @return
     */
    public int getCurrentPlayer();

    /**
     * Returns the number of players.
     *
     * @return
     */
    public int getQuantityOfPlayers();

    /**
     * Returns a score vector.
     * [1.0, 0.0] indicates a win for player 0.
     * [0.0, 1.0] indicates a win for player 1
     * [0.5, 0.5] indicates a draw
     * @return score array
     */
    public double[] getScore();

    /**
     * Returns an array of probability weights
     * for each move possible on this board. This
     * is only relevant in board states where
     * the choice to make is a random choice.
     * @return array of weights
     */
    public double[] getMoveWeights();

    public void bPrint();
}