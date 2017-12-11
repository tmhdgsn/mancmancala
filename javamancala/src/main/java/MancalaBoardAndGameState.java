public class MancalaBoardAndGameState {
    private MancalaBoard board;
    private GameState gameState;

    public MancalaBoardAndGameState(MancalaBoard board, GameState gameState) {

        this.board = board;
        this.gameState = gameState;
    }

    public MancalaBoard getBoard() {
        return board;
    }

    public GameState getGameState() {
        return gameState;
    }


}
