import random

from sneks.engine.core.direction import Direction
from sneks.engine.interface.snek import Snek


class CustomSnek(Snek):
    """
    This snek builds a list of directions that are not already
    occupied, and then chooses one randomly.
    """

    def get_next_direction(self) -> Direction:
        options = []

        for direction in Direction:
            if self.get_head().get_neighbor(direction) not in self.occupied:
                options.append(direction)

        if options:
            return random.choice(options)

        return Direction.UP
