from side import Side


def test_opposite():
    side = Side.NORTH

    assert side.opposite() == Side.SOUTH

    side = Side.SOUTH

    assert side.opposite() == Side.NORTH
