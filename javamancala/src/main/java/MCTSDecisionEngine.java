import java.util.*;

//class MCTSDecisionEngine extends DecisionEngine {
//    private double exploitConst = Math.sqrt(2);
//    private double negBias = 0.0;
//    private double posBias = 0.0;
//    private Random rnd;
//
//    MCTSDecisionEngine(Agent agent) {
//        super(agent);
//        this.rnd = new Random();
//    }
//
//    @Override
//    int getMove() {
//        int bestMove = 0;
//        GameState rootGameState = new GameState(agent.board, agent.side);
//        for (int i = 0; i < 12000; i++) {
//            select(agent.board.copy(), rootGameState);
//        }
//
//    }
//
//    private void select(MancalaBoard currentBoard, GameState currentGameState) {
//        MancalaBoardAndGameState data = policy(currentBoard, currentGameState);
//
//        double[] score = playout(data.getGameState(), data.getBoard());
//
//        GameState gameState = data.getGameState();
//        gameState.backpropagateScore(score);
//
//    }
//
//    private double[] runSimulation(GameState gameState, MancalaBoard board) {
//
//    }
//
//    private MancalaBoardAndGameState policy(MancalaBoard currentBoard, GameState currentGameState) {
//        while (!this.agent.board.gameOver()) {
//            if (currentGameState.side != null) {
//                if (currentGameState.unvisitedGameStates == null) {
//                    currentGameState.expandNode(currentBoard);
//                }
//
//                if (!currentGameState.unvisitedGameStates.isEmpty()) {
//                    GameState temp = currentGameState.unvisitedGameStates
//                            .remove(rnd.nextInt(currentGameState.unvisitedGameStates.size()));
//                    currentGameState.childGameStates.add(temp);
//                    agent.engine.playHole(temp.move, currentBoard, temp.side);
//                    return new MancalaBoardAndGameState(currentBoard, temp);
//                } else {
//                    ArrayList<GameState> bestGameStates
//                            = generateGameStates(currentGameState, currentBoard, posBias, negBias);
//                    if (bestGameStates.size() == 0) {
//                        return new MancalaBoardAndGameState(currentBoard, currentGameState);
//                    }
//
//                    GameState chosenGameState = bestGameStates.get(rnd.nextInt(bestGameStates.size()));
//                    currentGameState = chosenGameState;
//                    agent.engine.playHole(chosenGameState.move, currentBoard, chosenGameState.side);
//                }
//            } else {
//                if (currentGameState.unvisitedGameStates == null) {
//                    currentGameState.expandNode(currentBoard);
//                    for (GameState gs : currentGameState.unvisitedGameStates){
//                        gs.childGameStates.add(gs);
//                    }
//                    currentGameState.unvisitedGameStates.clear();
//                }
//
//                currentGameState = currentGameState.childGameStates.get(currentGameState.randomSelect());
//                agent.engine.playHole(currentGameState.move, currentGameState.board, currentGameState.side);
//            }
//        }
//        return new MancalaBoardAndGameState(currentBoard, currentGameState);
//    }
//
//    private double[] playout(GameState gameState, MancalaBoard board){
//        ArrayList<Integer> moves;
//        int mv;
//        MancalaBoard boardCopy = board.copy();
//
//        while(!agent.engine.gameOver(boardCopy)){
//
//        }
//    }
//
//
//    private ArrayList<GameState> generateGameStates(GameState gameState, MancalaBoard board, double posBias, double negBias) {
//        double bestScore = Double.NEGATIVE_INFINITY;
//        ArrayList<GameState> bestGameStates = new ArrayList<>();
//        for (GameState gs : gameState.childGameStates) {
//            double temporaryBest = gs.upperConfidenceBound(exploitConst) + posBias * gs.opti[gameState.side.value];
//            if (temporaryBest > bestScore) {
//                bestGameStates.clear();
//                bestGameStates.add(gs);
//                bestScore = temporaryBest;
//            } else if (temporaryBest == bestScore) {
//                bestGameStates.add(gs);
//            }
//        }
//
//        return bestGameStates;
//    }
//
//}
//
//

class MCTSDecisionEngine extends DecisionEngine {
    private HashMap<PlayedGameState, Integer> plays;
    private HashMap<PlayedGameState, Integer> wins;
    private final long calcTimeout = System.currentTimeMillis() + 4000;
    private final double exploitationCnst = Math.sqrt(2);
    private Random random;
    MCTSDecisionEngine(Agent agent) {
        super(agent);
        plays = new HashMap<>();
        wins = new HashMap<>();
        random = new Random();
    }

    @Override
    int getMove() {
        long begin = System.currentTimeMillis();
        MancalaBoard initState = agent.board;

        while (System.currentTimeMillis() - begin < this.calcTimeout) {
            this.runSimulation(initState);
        }

        ArrayList<MancalaMove> legalMoves = getLegalMoves(agent.board, agent.side);
        ArrayList<GameState> newGameStates = generateGameStates(agent.board, legalMoves, agent.side);
        return this.getBestMove(agent.side, newGameStates);
    }

    private void runSimulation(MancalaBoard initState) {
        boolean expand = true;
        HashMap<Integer, MancalaBoard> visitedStates = new HashMap<>();
        MancalaBoard state = initState;
        Side currentSide = agent.side;
        for (int i = 0; i < 100; i++) {
            ArrayList<MancalaMove> legalMoves = getLegalMoves(state, agent.side);
            ArrayList<GameState> newGameStates = generateGameStates(state, legalMoves, currentSide);

            boolean knowledgeKnown = false;
            for (GameState gs : newGameStates) {
                if (plays.containsKey(new PlayedGameState(gs.hashCode(), gs.side))) {
                    knowledgeKnown = true;
                }
            }
            if (knowledgeKnown) {
                int sum = 0;
                for (GameState gs : newGameStates) {
                    Side side = gs.side;
                    sum += plays.get(new PlayedGameState(gs.hashCode(), side));
                }
                double logTotal = Math.log(sum);

                ArrayList<BoundPlays> boundPlays = new ArrayList<>();
                for (GameState gs : newGameStates) {
                    Side side = gs.side;
                    double ucb = ucbValue(side, logTotal, gs);
                    boundPlays.add(new BoundPlays(ucb, gs.move, gs.board));
                }
                BoundPlays max = Collections.max(boundPlays, BoundPlays::compare);
                state = max.board;
                int move = max.move;

            } else {
                //make random move
                GameState choice = newGameStates.get(random.nextInt(newGameStates.size()));
                state = choice.board;
                Side side = choice.side;
            }

            visitedStates.put(state.hashCode(),state);
            //TODO finish runsim

        }
    }

    private int getBestMove(Side side, ArrayList<GameState> newGameStates) {
        HashMap<Double, Integer> stats = new HashMap<>();
        for (GameState gs : newGameStates) {
            int noWins = wins.getOrDefault(new PlayedGameState(gs.hashCode(), side), 0);
            int noPlays = plays.getOrDefault(new PlayedGameState(gs.hashCode(), side), 1);
            double score = noWins / noPlays;
            stats.put(score, gs.move);
        }
        Double max = Collections.max(stats.keySet());
        return stats.get(max) + 1;
    }

    private double ucbValue(Side side, double logTotal, GameState state) {
        double exploration = wins.getOrDefault(new PlayedGameState(state.hashCode(), side), 0)
                / plays.getOrDefault(new PlayedGameState(state.hashCode(), side), 1);
        double exploitation = exploitationCnst * Math.sqrt(logTotal / plays.get(new PlayedGameState(state.hashCode(), side)));
        return (exploitation + exploration) * (side == agent.side ? 1 : -1);
    }

    private ArrayList<GameState> generateGameStates(MancalaBoard board, ArrayList<MancalaMove> legalMoves, Side side) {
        ArrayList<GameState> newGameStates = new ArrayList<>();
        for (MancalaMove legalMove : legalMoves) {
            MancalaBoard boardCopy = board.copy();
            boolean ourTurn = this.playHole(legalMove.pit, boardCopy, side);
            Side newSide = ourTurn ? side : side.opposite();
            newGameStates.add(new GameState(boardCopy, legalMove.pit, newSide));
        }
        return newGameStates;
    }
}