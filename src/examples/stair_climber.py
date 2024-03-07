from sneks.engine.core.direction import Direction
from sneks.engine.interface.snek import Snek


class CustomSnek(Snek):
    """
    This snek alternates moving right and up by saving state
    between turns.
    """

    step: int = 0

    def get_next_direction(self) -> Direction:
        self.step += 1

        if self.step % 2:
            return Direction.UP
        else:
            return Direction.RIGHT
