public class BasicDecisionEngine extends DecisionEngine {
    public BasicDecisionEngine(Agent agent) {
        super(agent);
    }


    @Override
    public int getMove() {
        int[] board_side = this.agent.board.board[this.agent.side.value];
        for (int i = 0; i < MANCALA - 1; i++) {
            if (board_side[i] > 0) {
                return i + 1;
            }
        }
        return -1;
    }
}
