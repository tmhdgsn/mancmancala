import java.util.Scanner;

public class Agent {

    public final MancalaBoard board;
    public final DecisionEngine engine;
    public Side side;
    private boolean hasMoved;

    public Agent(DecisionEngine decisionEngine, int holes, int seeds) {
        this.board = new MancalaBoard(holes, seeds);
        this.engine = decisionEngine;
        this.side = Side.NORTH;
        this.hasMoved = false;
    }

    private static String[] getMessage(){
        Scanner sc = new Scanner(System.in);
        String fromEngine = sc.nextLine();
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
            String[] msgParts = Agent.getMessage();
            String msgType = msgParts[0];
            String args = msgParts[1];

            if (msgType.toUpperCase().equals("START")) {
                if (args.toUpperCase().equals("SOUTH")){
                    this.side = Side.NORTH;
                    ourTurn = true;
                }
            }

            if (msgType.toUpperCase().equals("END")){
                break;
            }

            if (msgType.toUpperCase().equals("CHANGE")){
                ourTurn = msgParts[msgParts.length - 1].toUpperCase().equals("YOU");
                this.board.updateBoard(msgParts.length - 2);
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