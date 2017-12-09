public enum Side {
    NORTH(0),
    SOUTH(1);

    public final int value;

    Side(int i) {
        value = i;
    }

    public Side opposite() {
        return this == Side.NORTH ? Side.SOUTH : Side.NORTH;
    }
}
