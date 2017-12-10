public class GameState {
    int noOfPlays;
    double score;
    GameState[] children;

    public GameState(MancalaBoard initBoard) {

    }

    public void selectAction(){

    }

    public void expand() {

    }

    public GameState select() {

    }

    public boolean isEndGameState() {
        return children == null;
    }

    public void updateGameStateScore(double value) {

    }

    public int getNoOfChildren() {
        return children == null ? 0 : children.length;
    }

}
