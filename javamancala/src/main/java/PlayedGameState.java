public class PlayedGameState {
    int stateHash;
    Side side;

    public PlayedGameState(int stateHash, Side side) {
        this.stateHash = stateHash;
        this.side = side;
    }
}
