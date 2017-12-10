import java.util.Random;

public class MCTSDecisionEngine extends DecisionEngine {
    private double exploitConst = Math.sqrt(2);
    private Random rnd;

    public MCTSDecisionEngine(Agent agent, Random rnd) {
        super(agent);
        this.rnd = rnd;
    }

    @Override
    int getMove() {
        return 0;
    }

    public MancalaMove runSimulation(MancalaBoard initBoard, int maxMoves) {
        GameState initGameState = new GameState(initBoard);
        MancalaMove bestMove = null;

        long initTime = System.nanoTime();

        for (int i = 0; i < maxMoves; i++) {

        }
    }

    private void select(MancalaBoard currentBoard, GameState currentGameState){

    }



}
