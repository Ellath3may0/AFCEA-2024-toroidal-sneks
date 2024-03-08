# TODO: Top c:
from sneks.engine.core.direction import Direction
from sneks.engine.interface.snek import Snek

'''
DISCLAIMER!!!

I code weird. I also mix up terms between languages very frequently. I also use TODO: tags as a sort of
table-of-contents for my programs. Just a few things to keep in mind.
   .-================-.
 //                    \\
||   BONUS DISCLAIMER   ||
 \\                    //
   '-================-'
                                                               - oooooooh look at that I made ASCII art c:
 I write comments mostly 
  for my own sake. The
 insults are directed at
 me, not any bystanders.
        Enjoy c:
              - Ella B.
'''




class CustomSnek(Snek):

    # Default 'mode'
    state: str = "search"

    # Variable for map class object
    mapObj = None

    # Persistent variable for where snek moved last call of get_next_direction()
    lastStep: Direction = None

    # Global step counter
    step = 0

    # Used as a switch for one-time initialisation code
    initialised = False

    # Hunt limit timer
    huntCounter = 0

    dangerData: list = None



    # TODO: get_next_direction(); snek movin method c:
    def get_next_direction(self) -> Direction:

        # Check is initialised
        # If not initialised...
        if not self.initialised:

            # Create a new, empty map
            self.mapObj = self.Map()

            # Making ABSOLUTELY CERTAIN that step is initialised correctly
            self.step = 1

            # Set snek to initialised
            self.initialised = True

            # Set state to default (just in case)
            state = "search"

            # Look around snek and fill in map
            self.mapFiller()

            # Mark snek's head as occupied
            self.mapObj.fillHead()

            # Telemetry key. I don't care how long the line is, its not worth trying to fit
            print("Telemetry key:\n[map]\n - H = Snek head\n - X = ignored occupied cell\n - [] = non-ignored occupied cell\n - . = unoccupied cell\n\nClosest target distance from head: [152 if no target selected]\nClosest target map pos [y, x]:     [30, 45 by default]\nClosest target occupied: - [if occupied, prints True]\nClosest target rPosY:    - [position of target cell relative to snek head (Y)]\nClosest target rPosX:    - [position of target cell relative to snek head (X)]\nClosest target ignore:   - [True if the cell is ignored by searcher/hunter]")

        # If initialised...
        else:
            # Another debug print
            print(self.lastStep)

            # Shift map relative to last snek movement
            self.mapObj.shiftMap(self.lastStep)

            # Look around snek and fill in map
            self.mapFiller()

            # Mark snek's head as occupied
            self.mapObj.fillHead()


            self.step += 1


        # Updating each cell's position relative to snek
        for i in range(60):
            for j in range(90):
                self.mapObj.map[i][j].updateRPos(i, j)

        # Get information about possible dangerous directions
        self.dangerData = self.mapObj.dangerData(self.lastStep)

    # TODO: get_next_direction().[debug printers] <----------------------------------------------------------------------

        # map

        for i in range(60):
            for j in range(90):
                if i == 30 and j == 45:
                    print("H", end=" ")
                else:
                    print(self.mapObj.map[i][j], end=" ")
            print()

        # Print danger zone

        for i in range(-2, 3):
            for j in range(-2, 3):
                if i == 0 and j == 0:
                    print("H", end=" ")
                else:
                    print(self.mapObj.map[30 + i][45 + j], end=" ")
            print()
        # lastStep
        '''
        print(self.lastStep)'''
        # dangerData
        '''
        print(self.dangerData)'''


        # Emergency mode changers
        # If all possible directions are dangerous,
        #  search for a possible exit
        '''if self.dangerData[0] >= 3:
            self.state == "escape"'''


        # TODO: get_next_direction().[Mode Callers]
        # When the snek hasn't found an enemy to attempt to trap,
        if self.state == "search":
            # wander diagonally (allows for checking 3 directions each step, filling out more map faster)
            return self.search()

        # When the snek has found an enemy to target
        if self.state == "hunt":
            return self.hunt()

        # If there are occupied cells in all directions around the snek, it
        #  will begin searching tighter pathways for possible escape routes.
        # Primary use case, if the snek reaches a possible dead end while hunting,
        #  it will turn around and squeeze between its own tail and the wall
        #  opposite the occupied-cell clump it was circling.
        if self.state == "escape":
            return self.escape()

        # If there are no escape routes, the snek will optimise its movement to use
        #  all available cells in its cocoon to weave through in an effort to
        #  outlast its opponents/live as long as possible.
        if self.state == "survive":
            return self.survive()

    # Search persistent variables
    # wander step
    searchStep = 0


    # Mode methods
    # TODO: Search mode: <==============================================================================================
    def search(self):
        # Switching to hunt condition
        # If snek finds a non-ignored, occupied cell, it will set it as target and switch to hunt mode
        # find nearest non self-spawned occupied cell
        lowestDistance = 152
        lowestIndices = [30, 45]
        for i in range(60):
            for j in range(90):
                if self.mapObj.map[i][j].occupied and \
                   not self.mapObj.map[i][j].ignore:
                    x = abs(self.mapObj.map[i][j].rPosX)
                    y = abs(self.mapObj.map[i][j].rPosY)
                    if x + y < lowestDistance:
                        lowestDistance = x + y
                        lowestIndices[0] = self.mapObj.map[i][j].rPosY
                        lowestIndices[1] = self.mapObj.map[i][j].rPosX

        '''
        print("Closest target distance from head:", lowestDistance)
        print("Closest target map pos [y, x]:    ", lowestIndices)
        print("Closest target occupied: -", self.mapObj.map[lowestIndices[0]][lowestIndices[1]].occupied,
              "\nClosest target rPosY:    -", self.mapObj.map[lowestIndices[0]][lowestIndices[1]].rPosY,
              "\nClosest target rPosX:    -", self.mapObj.map[lowestIndices[0]][lowestIndices[1]].rPosX,
              "\nClosest target ignore:   -", self.mapObj.map[lowestIndices[0]][lowestIndices[1]].ignore
              )'''

        if lowestDistance != 152:
            self.state = "hunt"
            self.huntCounter = 0
            self.huntStage = 'travel'
            return self.hunt(lowestIndices)

        # Move
        self.searchStep += 1
        if self.searchStep % 2 == 0:
            if self.isSafe(Direction.UP):
                print(self.isSafe(Direction.UP))
                self.lastStep = Direction.UP
            else:
                self.lastStep = self.searchShift(Direction.UP)
        else:
            if self.isSafe(Direction.RIGHT):
                print(self.isSafe(Direction.RIGHT))
                self.lastStep = Direction.RIGHT
            else:
                self.lastStep = self.searchShift(Direction.RIGHT)
        return self.lastStep


    # TODO: searchShift()
    def searchShift(self, direction: Direction) -> Direction:

        self.searchStep -= 1
        if self.look(Direction.LEFT) < 2:
            return Direction.UP
        if direction == Direction.UP:
            return Direction.LEFT
        elif direction == Direction.RIGHT:
            return Direction.UP
        else:
            raise ValueError("direction not valid")


    # Hunt stage variable
    huntStage = 'travel'

    # Hunt target cell
    targetCell = None

    # TODO: Hunting mode: <=============================================================================================
    def hunt(self, targetIndices = [30, 45]):
        self.huntCounter += 1
        if targetIndices != [30, 45]:
            self.targetCell = self.mapObj.map[targetIndices[0]][targetIndices[1]]


        # Check if danger is on more than one side.
            # If danger is on all sides,
            #     switch to escape mode
            # If danger is on the snek's left (relative to last step) and direction of origin,
            #     move in the direction clockwise from the direction of danger
            # If danger is on the snek's left side ("), direction of origin, and forward direction ("),
            #     move right (")
            # If danger is on the snek's left("), origin, and right("),
            #     move forward(")
            # If no danger to the snek's left,
            #     move left(")
        # Mark cells within 1/3 of step distance (use get distance from cell class) from original target of hunt
        # (lowestDistance from search) as ignore
        self.lastStep = Direction.UP
        return self.lastStep

    # TODO: Escape mode: <==============================================================================================
    def escape(self):
        print("placeholder")

    # TODO: Survive mode: <=============================================================================================
    def survive(self):
        print("placeholder")

    # Descriptions of all of these modes can be found in the get_next_direction
    #  method, in the section labeled "Mode Callers".

    # TODO: Map; cls;
    # Stores known information about the board
    class Map:

        # Map of all known filled in spaces
        map: list = None

        # Constructor
        def __init__(self):
            # Create content for numpy array
            tempArray = []
            for i in range(60):
                tempArray.append([])
                for j in range(90):
                    tempArray[i].append(self.myCell())

            # initialise numpy array
            self.map = tempArray


        # TODO: Map.myCell; cls
        # Class to store cell data
        class myCell:

            # Cell position relative to snek head
            rPosX: int = 0
            rPosY: int = 0

            # Cell occupied state (default False [snek can go there])
            occupied: bool = False

            # Is cell from my snek or a snek ruled as dead after hunt is complete
            ignore: bool = False

            def __init__(self):
                self.rPosX = 0
                self.rPosY = 0

                self.occupied = False
                self.ignore = False

            # Update relative position of cells
            def updateRPos(self, y, x):
                self.rPosX = -(45 - x)
                self.rPosY = -(30 - y)

            # To string for easy debug printing
            def __str__(self):
                # Read it yourself dummy
                if self.occupied:
                    if self.ignore:
                        return "x"
                    else:
                        return "□"
                else:
                    if self.ignore:
                        return "*"
                    else:
                        return "."

        # TODO: Map.fillCell()
        # Mark cell as occupied relative to snek head
        def fillCell(self, direction, distance: int) -> None:

            # Fix c:
            distance += 1

            # If block is certain to be occupied,
            if distance < 19:
                # Use direction of look to find occupied cell's location relative to snek
                if direction == Direction.UP:
                    self.map[30 - distance][45].occupied = True

                # ditto
                elif direction == Direction.LEFT:
                    self.map[30][45 - distance].occupied = True

                # ditto
                elif direction == Direction.RIGHT:
                    self.map[30][45 + distance].occupied = True

                # ditto
                elif direction == Direction.DOWN:
                    self.map[30 + distance][45].occupied = True
                else:
                    raise ValueError("Invalid direction")


        def fillHead(self):
            # Set cell where snek's head is to be occupied
            self.map[30][45].occupied = True
            self.map[30][45].ignore = True

        # TODO: Map.shiftMap()
        # Move the map relative to where the snek moved this step
        def shiftMap(self, lastStep: Direction) -> None:
            # Roll map relative to lastStep
            if lastStep == Direction.UP:
                # Save the last row
                temp: list = self.map[59]
                for i in range(59):
                    self.map[59 - i] = self.map[58 - i]
                self.map[0] = temp

            elif lastStep == Direction.LEFT:
                for i in range(60):
                    temp = self.map[i][89]
                    for j in range(89):
                        self.map[i][89 - j] = self.map[i][88 - j]
                    self.map[i][0] = temp

            elif lastStep == Direction.RIGHT:
                for i in range(60):
                    temp = self.map[i][0]
                    for j in range(89):
                        self.map[i][j] = self.map[i][j + 1]
                    self.map[i][89] = temp

            elif lastStep == Direction.DOWN:
                temp: list = self.map[0]
                for i in range(60):
                    self.map[i] = self.map[i + 1]
                self.map[59] = temp

            else:
                raise ValueError("Invalid direction")

        # TODO: Map.dangerData()
        # Return dangerous directions. Used in hunting mode to avoid getting trapped.
        def dangerData(self, lastStep) -> list:
            # Dangerous direction counter
            numDanger = 0

            # Which directions are dangerous?
            dangerousDirections = []

            # Traverse 5x5 cell space around snek head
            #  y traversal
            for i in range(-2, 3):
                #  x traversal
                for j in range(-2, 3):
                    if (
                        i == 0 and
                        j == 0
                    ):
                        continue

                    elif self.map[30 + i][45 + j].occupied:

                        # Dangerous square detected

                        # If the cell is not in a single direction (diagonal from head), add a second danger
                        # counter for both possible dangerous directions.
                        # At least one of these will evaluate to true on each calculation, because
                        #  a coordinate pair of [0, 0] has already been ruled out by the previous condition.
                        if i != 0:
                            numDanger += 1
                        if j != 0:
                            numDanger += 1

                        if i < 0:

                            try:
                                # If direction is not marked dangerous, throws value error
                                # If direction is marked dangerous, continues. Doesn't add to list,
                                #  and removes numDanger counter.
                                dangerousDirections.index(Direction.UP)
                                # Removes numDanger counter
                                numDanger -= 1

                            except ValueError:
                                # Marks direction as dangerous
                                dangerousDirections.append(Direction.UP)

                        elif i > 0:
                            try:
                                dangerousDirections.index(Direction.DOWN)
                                numDanger -= 1
                            except ValueError:
                                dangerousDirections.append(Direction.DOWN)

                        # I am not annotating these, it's the same as the last condition
                        if j < 0:
                            try:
                                dangerousDirections.index(Direction.LEFT)
                                numDanger -= 1
                            except ValueError:
                                dangerousDirections.append(Direction.LEFT)

                        elif j > 0:
                            try:
                                dangerousDirections.index(Direction.RIGHT)
                                numDanger -= 1
                            except ValueError:
                                dangerousDirections.append(Direction.RIGHT)

            # return number of hazardous directions, and a list containing the directions that are dangerous.
            print("")
            return [numDanger, dangerousDirections]


    # TODO: mapFiller()
    # Get results of snek.look() and use them to fill out the map
    def mapFiller(self) -> None:
        # Fill cell the return from snek.look(Dir*) for each direction
        self.mapObj.fillCell(Direction.UP, self.look(Direction.UP))
        self.mapObj.fillCell(Direction.LEFT, self.look(Direction.LEFT))
        self.mapObj.fillCell(Direction.DOWN, self.look(Direction.DOWN))
        self.mapObj.fillCell(Direction.RIGHT, self.look(Direction.RIGHT))


    # TODO: isSafe()
    def isSafe(self, direction) -> bool:
        for item in self.dangerData[1]:
            if item is direction:
                return False

        return True




# TODO: Bottom c:
