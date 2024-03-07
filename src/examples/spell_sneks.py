from sneks.engine.core.direction import Direction
from sneks.engine.interface.snek import Snek


class CustomSnek(Snek):
    """
    This snek makes a design based on a predetermined pattern.
    """

    letter = 0
    index = 0

    def get_next_direction(self) -> Direction:
        match self.letter:
            case 0:
                result = self.s()
            case 1:
                result = self.n()
            case 2:
                result = self.e()
            case 3:
                result = self.k()
            case 4:
                result = self.small_s()
            case _:
                return Direction.RIGHT
        self.index += 1
        return result

    def s(self) -> Direction:
        match self.index:
            case i if i < 1:
                return Direction.UP
            case i if 1 <= i < 2:
                return Direction.RIGHT
            case i if 2 <= i < 3:
                return Direction.DOWN
            case i if 3 <= i < 4:
                return Direction.RIGHT
            case i if 4 <= i < 5:
                return Direction.UP
            case i if 5 <= i < 6:
                return Direction.RIGHT
            case i if 6 <= i < 7:
                return Direction.DOWN
            case i if 7 <= i < 8:
                return Direction.RIGHT
            case i if 8 <= i < 12:
                return Direction.UP
            case i if 12 <= i < 16:
                return Direction.LEFT
            case i if 16 <= i < 21:
                return Direction.UP
            case i if 21 <= i < 26:
                return Direction.RIGHT
            case i if 26 <= i < 27:
                return Direction.DOWN
            case i if 27 <= i < 31:
                return Direction.LEFT
            case i if 31 <= i < 34:
                return Direction.DOWN
            case i if 34 <= i < 38:
                return Direction.RIGHT
            case i if 38 <= i < 43:
                return Direction.DOWN
            case i if 43 <= i < 44:
                return Direction.RIGHT
            case _:
                self.index = -1
                self.letter += 1
                return Direction.RIGHT

    def n(self) -> Direction:
        match self.index:
            case i if i < 5:
                return Direction.UP
            case i if 5 <= i < 6:
                return Direction.RIGHT
            case i if 6 <= i < 7:
                return Direction.DOWN
            case i if 7 <= i < 9:
                return Direction.RIGHT
            case i if 9 <= i < 13:
                return Direction.DOWN
            case i if 13 <= i < 14:
                return Direction.RIGHT
            case _:
                self.index = -1
                self.letter += 1
                return Direction.RIGHT

    def e(self) -> Direction:
        match self.index:
            case i if i < 4:
                return Direction.UP
            case i if 4 <= i < 7:
                return Direction.RIGHT
            case i if 7 <= i < 9:
                return Direction.DOWN
            case i if 9 <= i < 11:
                return Direction.LEFT
            case i if 11 <= i < 13:
                return Direction.DOWN
            case i if 13 <= i < 14:
                return Direction.RIGHT
            case i if 14 <= i < 16:
                return Direction.RIGHT
            case _:
                self.index = -1
                self.letter += 1
                return Direction.RIGHT

    def k(self) -> Direction:
        match self.index:
            case i if i < 8:
                return Direction.UP
            case i if 8 <= i < 9:
                return Direction.RIGHT
            case i if 9 <= i < 13:
                return Direction.DOWN
            case i if 13 <= i < 15:
                return Direction.RIGHT
            case i if 15 <= i < 17:
                return Direction.UP
            case i if 17 <= i < 18:
                return Direction.RIGHT
            case i if 18 <= i < 21:
                return Direction.DOWN
            case i if 21 <= i < 23:
                return Direction.LEFT
            case i if 23 <= i < 25:
                return Direction.DOWN
            case i if 25 <= i < 26:
                return Direction.RIGHT
            case i if 26 <= i < 27:
                return Direction.DOWN
            case i if 27 <= i < 28:
                return Direction.RIGHT
            case i if 28 <= i < 30:
                return Direction.RIGHT
            case _:
                self.index = -1
                self.letter += 1
                return Direction.RIGHT

    def small_s(self) -> Direction:
        match self.index:
            case i if 0 <= i < 3:
                return Direction.RIGHT
            case i if 3 <= i < 5:
                return Direction.UP
            case i if 5 <= i < 9:
                return Direction.LEFT
            case i if 9 <= i < 13:
                return Direction.UP
            case i if 13 <= i < 17:
                return Direction.RIGHT
            case i if 17 <= i < 18:
                return Direction.DOWN
            case i if 18 <= i < 21:
                return Direction.LEFT
            case i if 21 <= i < 23:
                return Direction.DOWN
            case i if 23 <= i < 27:
                return Direction.RIGHT
            case i if 27 <= i < 30:
                return Direction.DOWN
            case i if 30 <= i < 31:
                return Direction.RIGHT
            case _:
                self.index = -1
                self.letter += 1
                return Direction.RIGHT
