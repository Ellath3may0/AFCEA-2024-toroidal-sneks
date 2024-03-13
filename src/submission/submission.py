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

    # Danger data list
    dangerData: list = None

    # Extreme danger data list
    extremeDangerData: list = None



    # TODO: get_next_direction(); snek movin method c:
    def get_next_direction(self) -> Direction:

        # Check is initialised
        # If not initialised...
        if not self.initialised:

            # Create a new, empty map
            self.mapObj = self.Map()

            # Making ABSOLUTELY CERTAIN that step is initialised correctly
            self.step = 1

            # Set state to default (just in case)
            self.state = "search"

            # Set last step to default
            self.lastStep = Direction.UP

            # Look around snek and fill in map
            self.mapFiller()

            # Mark snek's head as occupied
            self.mapObj.fillHead()

            # Telemetry key. I don't care how long the line is, it's not worth trying to fit
            '''print("Telemetry key:\n[map]\n - H = Snek head\n - X = ignored occupied cell\n - [] = non-ignored occupied cell\n - . = unoccupied cell\n\nClosest target distance from head: [152 if no target selected]\nClosest target map pos [y, x]:     [30, 45 by default]\nClosest target occupied: - [if occupied, prints True]\nClosest target rPosY:    - [position of target cell relative to snek head (Y)]\nClosest target rPosX:    - [position of target cell relative to snek head (X)]\nClosest target ignore:   - [True if the cell is ignored by searcher/hunter]")'''

            # Set snek to initialised
            self.initialised = True

        # If initialised...
        else:
            # Shift map relative to last snek movement
            self.mapObj.shiftMap(self.lastStep)

            # Look around snek and fill in map
            self.mapFiller()

            # Mark snek's head as occupied
            self.mapObj.fillHead()


            self.step += 1


        # Updating each cell's position relative to snek
        for y in range(60):
            for x in range(90):
                self.mapObj.map[y][x].updateRPos(y, x)

        # Get information about possible dangerous directions
        self.dangerData = self.mapObj.dangerData()

        self.extremeDangerData = self.mapObj.extremeDangerData()

    # TODO: get_next_direction().[debug printers] <----------------------------------------------------------------------

        # map
        '''
        for i in range(60):
            for j in range(90):
                if i == 30 and j == 45:
                    print("H", end=" ")
                else:
                    print(self.mapObj.map[i][j], end=" ")
            print()'''

        # Map with relative positions
        '''
        for i in range(60):
            for j in range(90):
                print("(" + str("{:03d}".format(self.mapObj.map[i][j].rPosX) + ", " +
                    "{:03d}".format(self.mapObj.map[i][j].rPosY)), end=") "
                )
            print()'''
        # Print danger zone
        '''
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i == 0 and j == 0:
                    print("H", end=" ")
                else:
                    print(self.mapObj.map[30 + i][45 + j], end=" ")
            print()'''
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
            self.lastStep = self.search()
            return self.lastStep

        # When the snek has found an enemy to target
        if self.state == "hunt":
            self.lastStep = self.hunt()
            return self.lastStep

        # If there are occupied cells in all directions around the snek, it
        #  will begin searching tighter pathways for possible escape routes.
        # Primary use case, if the snek reaches a possible dead end while hunting,
        #  it will turn around and squeeze between its own tail and the wall
        #  opposite the occupied-cell clump it was circling.
        if self.state == "escape":
            self.lastStep = self.escape()
            return self.lastStep

        # If there are no escape routes, the snek will optimise its movement to use
        #  all available cells in its cocoon to weave through in an effort to
        #  outlast its opponents/live as long as possible.
        if self.state == "survive":
            self.lastStep = self.survive()
            return self.lastStep

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
                if (self.mapObj.map[i][j].occupied and
                   not self.mapObj.map[i][j].ignore
                ):
                    x = abs(self.mapObj.map[i][j].rPosX)
                    y = abs(self.mapObj.map[i][j].rPosY)
                    if x + y < lowestDistance:
                        lowestDistance = x + y
                        lowestIndices[0] = i
                        lowestIndices[1] = j

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
            self.huntStage = "travelA"
            self.huntStartPos = [30, 45]
            self.targetCell = self.mapObj.map[lowestIndices[0]][lowestIndices[1]]
            print(self.mapObj.map[lowestIndices[0]][lowestIndices[1]].rPosX, self.mapObj.map[lowestIndices[0]][lowestIndices[1]].rPosY)

        # I apologise... I wanted to avoid the nested if statements. I'll probably fix it later but my brain is too
        #  wired to take care of it now...

            # if the target is in the same column as the head & the target is above the head ***OR***
            # if the target is above the head & the target is farther horizontally than vertically
            if (
                    (self.targetCell.rPosX == 0 and
                    self.targetCell.rPosY > 0) or
                    (self.targetCell.rPosY > 0 and
                    abs(self.targetCell.rPosX) > abs(self.targetCell.rPosY))
            ):
                if self.targetCell.rPosX == 0:
                    self.huntStage = "travelB"

                # if direction is safe...
                if self.isSafe(Direction.UP):
                    return Direction.UP

                else:
                    self.state = "search"


            # if the target is in the same column as the head & the target is below the head ***OR***
            # if the target is below the head & the target is further horizontally than vertically
            elif (
                    (self.targetCell.rPosX == 0 and
                    self.targetCell.rPosY < 0) or
                    (self.targetCell.rPosY < 0 and
                    abs(self.targetCell.rPosX) > abs(self.targetCell.rPosY))
            ):
                if self.targetCell.rPosX == 0:
                    self.huntStage = "travelB"

                # if direction is safe
                if self.isSafe(Direction.DOWN):
                    return Direction.DOWN

                else:
                    self.state = "search"


            # if the target is left of the head & the target is in the same row as the head
            # if the target is left of the head & the target is further vertically than horizontal
            elif (
                    (self.targetCell.rPosX < 0 and
                    self.targetCell.rPosY == 0) or
                    (self.targetCell.rPosX < 0 and
                    abs(self.targetCell.rPosY) > abs(self.targetCell.rPosX)) or
                    (self.targetCell.rPosY == self.targetCell.rPosX and
                    self.targetCell.rPosX < 0)
            ):
                if self.targetCell.rPosY == 0:
                    self.huntStage = "travelB"

                # if direction is safe
                if self.isSafe(Direction.LEFT):
                    return Direction.LEFT

                else:
                    self.state = "search"


            # if the target is right of the head & the target is in the same row as the head
            # if the target is right of the head & the target is further vertically than horizontal
            elif (
                    (self.targetCell.rPosX > 0 and
                    self.targetCell.rPosY == 0) or
                    (self.targetCell.rPosX > 0 and
                    abs(self.targetCell.rPosY) > abs(self.targetCell.rPosX)) or
                    (self.targetCell.rPosY == self.targetCell.rPosX and
                    self.targetCell.rPosX > 0)
            ):
                if self.targetCell.rPosY == 0:
                    self.huntStage = "travelB"

                # if direction is safe
                if self.isSafe(Direction.RIGHT):
                    return Direction.RIGHT

                else:
                    self.state = "search"

# TODO: Replace "escape" states with the 'move-around-it' algorithm (idk what I'm doing)================================

        # Move
        self.searchStep += 1
        if self.searchStep % 2 == 0:
            if self.isSafe(Direction.UP):
                return Direction.UP
            else:
                return self.searchShift(Direction.UP)
        else:
            if self.isSafe(Direction.RIGHT):
                return Direction.RIGHT
            else:
                return self.searchShift(Direction.RIGHT)


    # TODO: searchShift()
    def searchShift(self, direction: Direction) -> Direction:

        self.searchStep -= 1
        if self.look(Direction.LEFT) < 2:
            return Direction.UP
        elif direction == Direction.UP:
            return Direction.LEFT
        elif direction == Direction.RIGHT:
            return Direction.UP
        else:
            raise ValueError("direction not valid")


    # Hunt stage variable
    huntStage = 'travelA'

    # Hunt target cell
    targetCell = None

    # Hunt limit timer
    huntCounter = 0

    # Hunt bounds
    huntBounds = [0, 0, 0, 0]

    # Hunt starting position
    huntStartPos = [0, 0]

    # Hunting bound tracker
    huntBoundTracker = [0, 0, 0, 0]

    # structSafeIgnore
    structSafeIgnore = False

    # Approach distances
    appDis1 = 91
    appDis2 = 91
    appDis3 = 91

    # TODO: Hunting mode: <=============================================================================================
    def hunt(self):
        self.huntCounter += 1
        if (self.extremeDangerData[0] > 2 and
            self.huntStage != 'cage' and not
            self.structSafeIgnore
        ):
            self.state = 'escape'
            return self.escape()

        # Stage 1 of travel
        # Make shorter distance translation
        if self.huntStage == "travelA":
            if self.lastStep == Direction.UP or self.lastStep == Direction.DOWN:
                # if reached correct position, switch to travel stage 2
                if self.targetCell.rPosY == 0:
                    self.huntStage = "travelB"
                    self.huntCounter = 0
                    return self.hunt()
                # else, continue travelling
                else:
                    try:
                        self.dangerData.index(self.lastStep)
                    except ValueError:
                        return self.lastStep
                    return self.escape()

            elif self.lastStep == Direction.RIGHT or self.lastStep == Direction.LEFT:
                # if reached correct position, switch to travel stage 2
                if self.targetCell.rPosX == 0:
                    self.huntStage = "travelB"
                    self.huntCounter = 0
                    return self.hunt()
                # else, continue travelling
                else:
                    try:
                        self.dangerData.index(self.lastStep)
                    except ValueError:
                        return self.lastStep
                    return self.escape()


        elif self.huntStage == "travelB":

            # While travelling straight...
            if self.huntCounter % 9 < 3 and not self.huntCounter == 0 and not self.structSafeIgnore:
                # if travelling horizontally and within cage range...
                if (
                    (self.lastStep == Direction.LEFT or
                    self.lastStep == Direction.RIGHT)
                        and
                    abs(self.targetCell.rPosX) < 3
                ):
                    self.appDis1 = 91
                    self.appDis2 = 91
                    self.appDis3 = 91
                    self.huntStage = "cage"
                    self.huntCounter = 0
                    return self.hunt()

                # if travelling vertically and within cage range...
                elif (
                    (self.lastStep == Direction.UP or
                    self.lastStep == Direction.DOWN)
                        and
                    abs(self.targetCell.rPosY) < 3
                ):
                    self.appDis1 = 91
                    self.appDis2 = 91
                    self.appDis3 = 91
                    self.huntStage = "cage"
                    self.huntCounter = 0
                    return self.hunt()

                # if the target is right of head...
                elif (
                    self.targetCell.rPosX > 0
                ):
                    return Direction.RIGHT

                # if the target is below the head...
                elif (
                    self.targetCell.rPosY < 0
                ):
                    return Direction.DOWN

                # if the target is left of head...
                elif (
                    self.targetCell.rPosX < 0
                ):
                    return Direction.LEFT

                # if the target is above the head...
                elif (
                    self.targetCell.rPosY > 0
                ):
                    return Direction.UP

            # This part is difficult to explain. It's creating a search window 3 cells wide
            # to give itself more information about the location it's approaching
            '''
            The snek moves like this (relative to direction it's moving):
            O X>X
                V
            X<X<X
            V
            X>X O
              V
            O X O
            '''
            if self.huntCounter % 9 == 3:
                self.structSafeIgnore = True
                if (
                    ((self.lastStep == Direction.LEFT or
                    self.lastStep == Direction.RIGHT) and
                    abs(self.targetCell.rPosX) < 4)

                        or

                    ((self.lastStep == Direction.UP or
                    self.lastStep == Direction.DOWN) and
                    abs(self.targetCell.rPosY) < 4)
                ):
                    self.huntCounter = 1
                    return self.hunt()
                return self.getRelativeDirection(Direction.LEFT)

            elif self.huntCounter % 9 == 4:
                return self.getRelativeDirection(Direction.RIGHT)

            elif self.huntCounter % 9 == 5:
                temp = self.look(self.getRelativeDirection(Direction.UP))
                if temp < 19:
                    self.appDis1 = temp
                return self.getRelativeDirection(Direction.RIGHT)

            elif self.huntCounter % 9 == 6:
                return self.getRelativeDirection(Direction.UP)

            elif self.huntCounter % 9 == 7:
                return self.getRelativeDirection(Direction.LEFT)

            elif self.huntCounter % 9 == 8:
                temp = self.look(self.getRelativeDirection(Direction.UP))
                if temp < 19:
                    self.appDis3 = temp + 1
                return self.getRelativeDirection(Direction.LEFT)

            elif self.huntCounter % 9 == 0:
                temp = self.look(self.getRelativeDirection(Direction.RIGHT))
                if temp < 19:
                    self.appDis2 = temp + 1

                if (
                    self.appDis1 < self.appDis2 or
                    self.appDis3 < self.appDis2
                ):
                    if self.appDis2 > self.appDis3:
                        self.appDis2 = self.appDis3

                    if self.appDis2 > self.appDis1:
                        self.appDis2 = self.appDis1
                        self.appDis3 = self.appDis1

                    self.targetCell = self.mapObj.fillCell(self.getRelativeDirection(Direction.RIGHT), self.appDis2 - 1)

                self.structSafeIgnore = False
                return self.getRelativeDirection(Direction.RIGHT)

        elif self.huntStage == "cage":
            print("Called 'cage' mode")

            # Cage building sequence
            if self.huntCounter == 1:
                return self.getRelativeDirection(Direction.UP)

            elif self.huntCounter in range(2, 4):
                return self.getRelativeDirection(Direction.RIGHT)

            elif self.huntCounter == 4:
                self.huntStage = "circle"
                self.huntCounter = 0
                return self.getRelativeDirection(Direction.LEFT)


        elif self.huntStage == "circle":
            print("Called 'circle' mode")
            # If danger is on the snek's left (relative to last step) and direction of origin,
            #     move in the direction clockwise from the direction of danger
            # If danger is on the snek's left side ("), direction of origin, and forward direction ("),
            #     move right (")
            # If danger is on the snek's left("), origin, and right("),
            #     move forward(")
            # If no danger to the snek's left,
            #     move left(")



        # Check if extreme danger is on more than one side (unless building structure) ----DONE
            # If danger is on all sides, ----DONE
            #     switch to escape mode ----DONE
        # All of this is for inside circle I need to plan for the other modes

        # Mark cells within 1/3 of step distance (use get distance from cell class) from original target of hunt
        # (lowestDistance from search) as ignore
        return self.lastStep

    # TODO: Escape mode: <==============================================================================================
    def escape(self):
        print("Called 'survive' mode")
        return self.lastStep

    # TODO: Survive mode: <=============================================================================================
    def survive(self):
        print("Called 'survive' mode")
        return self.lastStep

    # Descriptions of all of these modes can be found in the get_next_direction
    #  method, in the section labeled "Mode Callers".

    # TODO: getRelativeDirection()
    # Returns input direction relative to the snek
    # - UP = FORWARD
    # - DOWN = BACKWARD
    def getRelativeDirection(self, directIn: Direction) -> Direction:
        if self.lastStep == Direction.UP:
            if directIn == Direction.UP:
                return Direction.UP
            elif directIn == Direction.LEFT:
                return Direction.LEFT
            elif directIn == Direction.RIGHT:
                return Direction.RIGHT
            elif directIn == Direction.DOWN:
                return Direction.DOWN
            else:
                raise ValueError("Invalid direction")

        elif self.lastStep == Direction.LEFT:
            if directIn == Direction.UP:
                return Direction.LEFT
            elif directIn == Direction.LEFT:
                return Direction.DOWN
            elif directIn == Direction.RIGHT:
                return Direction.UP
            elif directIn == Direction.DOWN:
                return Direction.RIGHT
            else:
                raise ValueError("Invalid Direction")

        elif self.lastStep == Direction.RIGHT:
            if directIn == Direction.UP:
                return Direction.RIGHT
            elif directIn == Direction.LEFT:
                return Direction.UP
            elif directIn == Direction.RIGHT:
                return Direction.DOWN
            elif directIn == Direction.DOWN:
                return Direction.LEFT
            else:
                raise ValueError("Invalid direction")

        elif self.lastStep == Direction.DOWN:
            if directIn == Direction.UP:
                return Direction.DOWN
            elif directIn == Direction.LEFT:
                return Direction.RIGHT
            elif directIn == Direction.RIGHT:
                return Direction.LEFT
            elif directIn == Direction.DOWN:
                return Direction.UP
            else:
                raise ValueError("Invalid direction")

        else:
            raise ValueError("lastStep broken :/")


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
            def updateRPos(self, y: int, x: int):
                self.rPosX = x - 45
                self.rPosY = -(y - 30)

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
        def fillCell(self, direction, distance: int):

            # fix c: (Don't delete it. This isn't the source of your problem. We've done this five times now.)
            distance += 1

            # If block is certain to be occupied,
            if distance < 19:
                # Use direction of look to find occupied cell's location relative to snek
                if direction == Direction.UP:
                    self.map[30 - distance][45].occupied = True
                    return self.map[30 - distance][45]

                # ditto
                elif direction == Direction.LEFT:
                    self.map[30][45 - distance].occupied = True
                    return self.map[30][45 - distance]

                # ditto
                elif direction == Direction.RIGHT:
                    self.map[30][45 + distance].occupied = True
                    return self.map[30][45 + distance]

                # ditto
                elif direction == Direction.DOWN:
                    self.map[30 + distance][45].occupied = True
                    return self.map[30 + distance][45]
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
                for i in range(59):
                    self.map[i] = self.map[i + 1]
                self.map[59] = temp

            else:
                raise ValueError("Invalid direction")

        # TODO: Map.dangerData()
        # Return dangerous directions. Used in hunting mode to avoid getting trapped.
        def dangerData(self) -> list:
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
            return [numDanger, dangerousDirections]

        # TODO: extremeDangerData()
        def extremeDangerData(self) -> list:
            # Dangerous direction counter
            numDanger = 0

            # Which directions are dangerous?
            dangerousDirections = []

            # Traverse 3x3 cell space around snek head
            #  y traversal
            for i in range(-1, 2):
                #  x traversal
                for j in range(-1, 2):
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
        if direction in self.dangerData:
            return False
        return True




# TODO: Bottom c:
