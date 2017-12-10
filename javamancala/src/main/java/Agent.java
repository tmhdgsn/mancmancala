import java.util.Scanner;

public class Agent {

    public final MancalaBoard board;
    public final DecisionEngine engine;
    public Side side;
    private boolean hasMoved;
    private Scanner sc;

    public Agent(String decisionEngine, int holes, int seeds, Scanner sc) {
        this.sc = sc;
        DecisionEngineFactory factory = new DecisionEngineFactory(this);
        this.board = new MancalaBoard(holes, seeds);

        if (factory.engines.containsKey(decisionEngine)){
            this.engine = factory.engines.get(decisionEngine);
        } else {
            this.engine = factory.engines.get("basic");
        }

        this.side = Side.NORTH;
        this.hasMoved = false;
    }

    private String[] getMessage(){
        String fromEngine = this.sc.nextLine();
        // TODO: Log output for debugging.
        return fromEngine.split(";");
    }

    private void playMove(int move){
        String msg;
        if (move == -1) {
            msg = "SWAP";
            this.side = this.side.opposite();
        } else {
            msg = String.format("MOVE;%d", move);
        }
        System.out.println(msg);
    }

    public void play(){
        boolean ourTurn = false;
        while (true) {
            String[] msgParts = this.getMessage();
            String msgType = msgParts[0];

            if (msgType.toUpperCase().equals("END")){
                break;
            }

            String args = msgParts[1];
            if (msgType.toUpperCase().equals("START")) {
                if (args.toUpperCase().equals("SOUTH")){
                    this.side = Side.SOUTH;
                    ourTurn = true;
                }
            }

            if (msgType.toUpperCase().equals("CHANGE")){
                ourTurn = msgParts[msgParts.length - 1].toUpperCase().equals("YOU");
                this.board.updateBoard(msgParts[msgParts.length - 2]);
                if (args.toUpperCase().equals("SWAP")){
                    this.side = this.side.opposite();
                }
                //TODO: log output here for debug
            }
            if (ourTurn) {
                int move = this.engine.getMove();
                this.playMove(move);
                this.hasMoved = true;
            }
        }
    }
}