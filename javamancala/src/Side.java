public enum Side {
    NORTH,
    SOUTH;

    public Side opposite() {
        return this == Side.NORTH ? Side.SOUTH : Side.NORTH;
    }
}
