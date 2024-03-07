from sneks.engine.core.direction import Direction
from sneks.engine.interface.snek import Snek


class CustomSnek(Snek):
    """
    This snek wants to go up, unless it sees something
    in front of it. It only knows how to avoid obstacles
    by going right.
    """

    def get_next_direction(self) -> Direction:
        if self.look(Direction.UP) < 5:
            return Direction.RIGHT
        return Direction.UP
