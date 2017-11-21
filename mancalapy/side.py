from enum import Enum


class Side(Enum):
    NORTH = 0
    SOUTH = 1

    def opposite(self):
        return Side.SOUTH if self == Side.NORTH else Side.NORTH
