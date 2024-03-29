# TODO: Top c:
from sneks.engine.core.direction import Direction
from sneks.engine.interface.snek import Snek

import random as r

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
        #for y in range(60):
        #    for x in range(90):
        #        self.mapObj.map[y][x].updateRPos(y, x)

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
            print()
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


        # TODO: get_next_direction().[Mode Callers]
        # When the snek hasn't found an enemy to attempt to trap,
        if self.state == "search":
            # wander diagonally (allows for checking 3 directions each step, filling out more map faster)
            self.lastStep = self.search()

        # When the snek has found an enemy to target
        if self.state == "hunt":
            self.lastStep = self.hunt()

        # If there are no escape routes, the snek will optimise its movement to use
        #  all available cells in its cocoon to weave through in an effort to
        #  outlast its opponents/live as long as possible.
        if self.state == "survive":
            self.lastStep = self.survive()

        # Updating each cell's accessibility
        self.mapObj.updateAccess()

        return self.lastStep

    # Search persistent variables
    # wander step
    searchStep = 0


    # Mode methods
    # TODO: Search mode: <==============================================================================================
    def search(self):
        self.tbClose = False


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
                    self.mapObj.map[i][j].updateRPos(i, j)
                    x = abs(self.mapObj.map[i][j].rPosX)
                    y = abs(self.mapObj.map[i][j].rPosY)
                    if x + y < lowestDistance:
                        lowestDistance = x + y
                        lowestIndices[0] = i
                        lowestIndices[1] = j



        if lowestDistance != 152:
            self.state = "hunt"
            self.huntCounter = 0
            self.huntStage = "travelA"
            self.huntStartPos = [30, 45]
            self.targetCell = self.mapObj.map[lowestIndices[0]][lowestIndices[1]]
            # print(self.mapObj.map[lowestIndices[0]][lowestIndices[1]].rPosX, self.mapObj.map[lowestIndices[0]][lowestIndices[1]].rPosY)


            # if the target is in the same column as the head & the target is above the head
            # ***OR***
            # if the target is above the head & the target is farther horizontally than vertically

            if (
                (self.targetCell.rPosX == 0 and
                self.targetCell.rPosY > 0) or
                (self.targetCell.rPosY > 0 and
                abs(self.targetCell.rPosX) > abs(self.targetCell.rPosY))
            ):
                if self.targetCell.rPosX == 0:
                    self.huntStage = "preTravelB"
                    return self.hunt()


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
                    self.huntStage = "preTravelB"
                    return self.hunt()

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
                    self.huntStage = "preTravelB"
                    return self.hunt()

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
                    self.huntStage = "preTravelB"
                    return self.hunt()

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

    ptbInitDir = None

    tbClose = False

    cageDir = False

    # TODO: Hunting mode: <=============================================================================================
    def hunt(self):
        #print(self.targetCell.rPosX, self.targetCell.rPosY)
        self.huntCounter += 1

        for i in range(60):
            for j in range(90):
                if self.mapObj.map[i][j] is self.targetCell:
                    self.targetCell.updateRPos(i, j)

        # Stage 1 of travel
        # Make shorter distance translation
        if self.huntStage == "travelA":
            #print("travelA")


            if self.lastStep == Direction.UP or self.lastStep == Direction.DOWN:
                # if reached correct position, switch to travel stage 2
                if self.targetCell.rPosY == 0:
                    self.huntStage = "preTravelB"
                    self.huntCounter = 0
                    return self.hunt()
                # else, continue travelling
                else:
                    try:
                        self.dangerData.index(self.lastStep)
                    except ValueError:
                        return self.lastStep
                    self.state = "survive"
                    return self.survive()

            elif self.lastStep == Direction.RIGHT or self.lastStep == Direction.LEFT:
                # if reached correct position, switch to travel stage 2
                if self.targetCell.rPosX == 0:
                    self.huntStage = "preTravelB"
                    self.huntCounter = 0
                    return self.hunt()
                # else, continue travelling
                else:
                    try:
                        self.dangerData.index(self.lastStep)
                    except ValueError:
                        return self.lastStep
                    self.state = "survive"
                    return self.survive()


        elif self.huntStage == "preTravelB":
            #print("Called preTravelB")
            for i in range(60):
                for j in range(90):
                    if self.mapObj.map[i][j] is self.targetCell:
                        self.targetCell.updateRPos(i, j)

            if self.mapObj.look(self.getTargetCellDirection()) < 2 and self.huntCounter == 1:
                if self.mapObj.look(self.getRelativeDirection(Direction.RIGHT, self.getTargetCellDirection())) == 0:
                    self.cageDir = True
                else:
                    self.cageDir = False
                self.huntStage = "circle"
                self.huntCounter = 0
                return self.hunt()

            elif self.mapObj.look(self.getTargetCellDirection()) < 6:
                self.tbClose = True
                if self.huntCounter == 1:
                    if self.mapObj.look(self.getRelativeDirection(Direction.RIGHT, self.getTargetCellDirection())) != 0:
                        self.ptbInitDir = Direction.RIGHT
                        return self.getRelativeDirection(Direction.RIGHT, self.getTargetCellDirection())

                    elif self.mapObj.look(self.getRelativeDirection(Direction.LEFT, self.getTargetCellDirection())) == 0:
                        self.appDis1 = 91
                        self.huntCounter = 0
                        self.tbClose = False
                        self.huntStage = "travelB"
                        return self.hunt()

                    else:
                        self.ptbInitDir = Direction.LEFT
                        return self.getRelativeDirection(Direction.LEFT, self.getTargetCellDirection())

                elif self.huntCounter == 2:
                    if \
                        (self.getTargetCellDirection() == Direction.UP or
                        self.getTargetCellDirection() == Direction.DOWN) and \
                        self.look(self.getTargetCellDirection()) <= abs(self.targetCell.rPosY)\
                    :
                        self.appDis1 = self.look(self.getTargetCellDirection()) - 1

                    elif \
                        (self.getTargetCellDirection() == Direction.RIGHT or
                        self.getTargetCellDirection() == Direction.LEFT) and \
                        self.look(self.getTargetCellDirection()) < abs(self.targetCell.rPosX)\
                    :
                        self.appDis1 = self.look(self.getTargetCellDirection()) - 1

                    return self.getTargetCellDirection()

                elif self.huntCounter == 3:
                    if self.ptbInitDir == Direction.LEFT:
                        return self.getRelativeDirection(Direction.RIGHT, self.getTargetCellDirection())
                    else:
                        return self.getRelativeDirection(Direction.LEFT, self.getTargetCellDirection())

                else:
                    if self.appDis1 != 91:
                        self.mapObj.fillCell(self.getTargetCellDirection(), self.appDis1)

                    self.appDis1 = 91
                    self.huntCounter = 0
                    self.huntStage = "travelB"
                    return self.hunt()

            else:
                self.tbClose = False
                self.huntCounter = 0
                self.huntStage = "travelB"
                return self.hunt()


        elif self.huntStage == "travelB":
            #print("travelB")

            # While travelling straight...
            if self.huntCounter % 9 < 3 and not self.huntCounter == 0:
                #print(self.huntCounter % 9)
                if self.mapObj.look(self.getTargetCellDirection()) < 3:
                    self.appDis1 = 91
                    self.appDis2 = 91
                    self.appDis3 = 91
                    self.huntStage = "cage"
                    self.huntCounter = 0
                    return self.hunt()

                return self.getTargetCellDirection()

            # This part is difficult to explain. It's creating a search window 3 cells wide
            # to give itself more information about the location it's approaching
            '''
            The snek moves like this (relative to direction it's moving):
            O   X > X
                    V
            X < X < X
            V
            X > X   O
                V
            O   X   O
            '''
            if self.huntCounter % 9 == 3:
                self.structSafeIgnore = True
                if self.look(self.getTargetCellDirection()) < 6:
                    self.huntCounter = 0
                    return self.hunt()

                return self.getRelativeDirection(Direction.LEFT)

            elif self.huntCounter % 9 == 4:
                return self.getRelativeDirection(Direction.RIGHT)

            elif self.huntCounter % 9 == 5:
                temp = self.look(self.getRelativeDirection(Direction.UP))
                if temp < 19:
                    self.appDis1 = temp - 1
                return self.getRelativeDirection(Direction.RIGHT)

            elif self.huntCounter % 9 == 6:
                return self.getRelativeDirection(Direction.UP)

            elif self.huntCounter % 9 == 7:
                return self.getRelativeDirection(Direction.LEFT)

            elif self.huntCounter % 9 == 8:
                temp = self.look(self.getRelativeDirection(Direction.UP))
                if temp < 19:
                    self.appDis3 = temp
                return self.getRelativeDirection(Direction.LEFT)

            elif self.huntCounter % 9 == 0:
                temp = self.look(self.getRelativeDirection(Direction.RIGHT))
                if temp < 19:
                    self.appDis2 = temp

                if (
                    self.appDis1 < self.appDis2 or
                    self.appDis3 < self.appDis2
                ):
                    if self.appDis2 > self.appDis3:
                        self.appDis2 = self.appDis3

                    if self.appDis2 > self.appDis1:
                        self.appDis2 = self.appDis1
                        self.appDis3 = self.appDis1

                    self.mapObj.fillCell(self.getRelativeDirection(Direction.RIGHT), self.appDis2)
                    if self.getRelativeDirection(Direction.RIGHT) == Direction.LEFT:
                        self.targetCell = self.mapObj.map[30][44 - self.appDis2]
                    elif self.getRelativeDirection(Direction.RIGHT) == Direction.UP:
                        self.targetCell = self.mapObj.map[29 - self.appDis2]
                    elif self.getRelativeDirection(Direction.RIGHT) == Direction.RIGHT:
                        self.targetCell = self.mapObj.map[30][46 + self.appDis2]
                    elif self.getRelativeDirection(Direction.RIGHT) == Direction.DOWN:
                        self.targetCell = self.mapObj.map[31 + self.appDis2][45]

                self.structSafeIgnore = False
                return self.getRelativeDirection(Direction.RIGHT)

        elif self.huntStage == "cage":

            #print("Called 'cage' mode")
            self.circlePosStepper()
            print(self.huntCounter)

            if self.huntCounter == 1:
                self.cageDir = False
                self.huntCounter = 3 - self.mapObj.look(self.getTargetCellDirection())

            # Cage building sequence
            if self.huntCounter in range(1, 3):
                return self.getRelativeDirection(Direction.UP, self.getTargetCellDirection())

            elif self.huntCounter == 3:
                left = self.mapObj.look(self.getRelativeDirection(Direction.LEFT, self.getTargetCellDirection()))
                right = self.mapObj.look(self.getRelativeDirection(Direction.RIGHT, self.getTargetCellDirection()))

                if left != 0 and right != 0:
                    self.cageDir = bool(r.getrandbits(1))

                elif left == 0:
                    self.cageDir = False

                elif right == 0:
                    self.cageDir = True

                if self.cageDir:
                    return self.getRelativeDirection(Direction.LEFT, self.getTargetCellDirection())
                else:
                    return self.getRelativeDirection(Direction.RIGHT, self.getTargetCellDirection())

            if not self.cageDir:

                if self.huntCounter == 4:
                    return self.getRelativeDirection(Direction.RIGHT)

                elif self.huntCounter == 5:
                    self.huntCounter = 0
                    if self.look(self.getRelativeDirection(Direction.LEFT)) == 0:
                        self.huntStage = "cageAlt"
                        return self.hunt()
                    self.huntStage = "circle"
                    return self.getRelativeDirection(Direction.LEFT)

            else:

                if self.huntCounter == 4:
                    return self.getRelativeDirection(Direction.LEFT)

                elif self.huntCounter == 5:
                    self.huntCounter = 0
                    if self.look(self.getRelativeDirection(Direction.RIGHT)) == 0:
                        self.huntStage = "cageAlt"
                        return self.hunt()
                    self.huntStage = "circle"
                    return self.getRelativeDirection(Direction.RIGHT)


        elif self.huntStage == "cageAlt":
            if self.huntCounter == 1:
                return self.getRelativeDirection(Direction.UP)

            elif self.huntCounter == 2 and self.cageDir == False:
                if self.look(self.getRelativeDirection(Direction.LEFT)) == 0:
                    self.state = "survive"
                    return self.survive()
                self.huntStage = "circle"
                self.huntCounter = 0
                return self.getRelativeDirection(Direction.LEFT)

            else:
                if self.look(self.getRelativeDirection(Direction.RIGHT)) == 0:
                    self.state = "survive"
                    return self.survive()
                self.huntStage = "circle"
                self.huntCounter = 0
                return self.getRelativeDirection(Direction.RIGHT)


        elif self.huntStage == "circle":
            #print("Called 'circle' mode")
            self.circlePosStepper()


            if not self.cageDir:
                if (
                    not self.leftSafe() and
                    not self.rightSafe() and
                    not self.forwardSafe() and
                    not self.backwardSafe() # hehe I used it
                ):
                    self.state = "survive"
                    return self.survive()

                elif (
                    self.forwardSafe() and
                    not self.leftSafe() and
                    not self.rightSafe()
                ):
                    self.lastStep = self.getRelativeDirection(Direction.UP)


                elif (
                    self.forwardSafe() and
                    not self.leftSafe() and
                    self.mapObj.look(self.getRelativeDirection(Direction.LEFT)) > 0 and
                    self.rightSafe()
                ):
                    self.lastStep = self.getRelativeDirection(Direction.UP)


                elif (self.mapObj.look(self.getRelativeDirection(Direction.LEFT)) < 2 and
                    self.mapObj.look(self.getRelativeDirection(Direction.RIGHT)) > 0
                ):
                    self.lastStep = self.getRelativeDirection(Direction.RIGHT)


                # If danger is to the snek's front, left, and rear...
                elif (
                        not self.forwardSafe() and
                        not self.leftSafe() and
                        self.rightSafe()
                ):
                    self.lastStep = self.getRelativeDirection(Direction.RIGHT)


                elif (
                    self.forwardSafe() and
                    not self.rightSafe() and
                    self.leftSafe() and
                    self.q2safe()
                ):
                    self.lastStep = self.getRelativeDirection(Direction.LEFT)

                # If snake is heading towards danger...
                elif (
                    not self.forwardSafe() and
                    self.look(self.getRelativeDirection(Direction.RIGHT)) > 0
                ):
                    self.lastStep = self.getRelativeDirection(Direction.RIGHT)


                # If danger is only on the snek's left...
                elif (
                    self.q1safe() and
                    self.forwardSafe()
                    and self.rightSafe() and
                    not self.leftSafe() and
                    not self.q3safe()
                ):
                    # move forward (rel*)
                    self.lastStep = self.getRelativeDirection(Direction.UP)

                elif (
                    not self.q2safe() and
                    self.leftSafe() and
                    self.rightSafe() and
                    self.forwardSafe()
                ):
                    self.lastStep = self.getRelativeDirection(Direction.RIGHT)

                elif self.mapObj.look(self.getRelativeDirection(Direction.LEFT)) > 0 and self.q2safe():
                    self.lastStep = self.getRelativeDirection(Direction.LEFT)

                else:
                    print("no case has been found ===================================")
                    self.state = "survive"
                    return self.survive()

                if self.lastStep == self.getRelativeDirection(Direction.RIGHT):
                    if (
                        self.lastStep == Direction.UP and
                        self.mapObj.map[29 - self.mapObj.look(Direction.UP)][45].ignore and
                        self.mapObj.look(Direction.RIGHT) > 0
                    ):
                            self.lastStep = Direction.RIGHT
                    elif (
                        self.lastStep == Direction.RIGHT and
                        self.mapObj.map[30][46 + self.mapObj.look(Direction.RIGHT)].ignore and
                        self.mapObj.look(Direction.DOWN) > 0
                    ):
                        self.lastStep = Direction.DOWN
                    elif (
                        self.lastStep == Direction.LEFT and
                        self.mapObj.map[30][44 - self.mapObj.look(Direction.LEFT)].ignore and
                        self.mapObj.look(Direction.UP) > 0
                    ):
                        self.lastStep = Direction.UP
                    elif (
                        self.lastStep == Direction.DOWN and
                        self.mapObj.map[31 + self.mapObj.look(Direction.DOWN)].ignore and
                        self.mapObj.look(Direction.LEFT) > 0
                    ):
                        self.lastStep = Direction.LEFT


            else:

                if (
                        not self.leftSafe() and
                        not self.rightSafe() and
                        not self.forwardSafe() and
                        not self.backwardSafe()  # hehe I used it
                ):
                    self.state = "survive"
                    return self.survive()

                elif (
                        self.forwardSafe() and
                        not self.leftSafe() and
                        not self.rightSafe()
                ):
                    self.lastStep = self.getRelativeDirection(Direction.UP)

                elif (
                    self.forwardSafe() and
                    self.leftSafe() and
                    self.mapObj.look(self.getRelativeDirection(Direction.RIGHT)) > 0 and
                    not self.rightSafe()
                ):
                    self.lastStep = self.getRelativeDirection(Direction.UP)

                elif (self.mapObj.look(self.getRelativeDirection(Direction.RIGHT)) < 2 and
                      self.mapObj.look(self.getRelativeDirection(Direction.LEFT)) > 0
                ):
                    self.lastStep = self.getRelativeDirection(Direction.LEFT)


                # If danger is to the snek's front, right, and rear...
                elif (
                        not self.forwardSafe() and
                        not self.rightSafe() and
                        self.leftSafe()
                ):
                    self.lastStep = self.getRelativeDirection(Direction.LEFT)

                elif (
                        self.forwardSafe() and
                        not self.leftSafe() and
                        self.rightSafe() and
                        self.q1safe()
                ):
                    self.lastStep = self.getRelativeDirection(Direction.RIGHT)

                # If snake is heading towards danger...
                elif (
                        not self.forwardSafe() and
                        self.look(self.getRelativeDirection(Direction.LEFT)) > 0
                ):
                    self.lastStep = self.getRelativeDirection(Direction.LEFT)


                # If danger is only on the snek's right...
                elif (
                        self.q2safe() and
                        self.forwardSafe() and
                        not self.rightSafe() and
                        self.leftSafe() and
                        not self.q4safe()
                ):
                    # move forward (rel*)
                    self.lastStep = self.getRelativeDirection(Direction.UP)

                elif (
                        not self.q1safe() and
                        self.leftSafe() and
                        self.rightSafe() and
                        self.forwardSafe()
                ):
                    self.lastStep = self.getRelativeDirection(Direction.LEFT)

                elif self.mapObj.look(self.getRelativeDirection(Direction.RIGHT)) > 0 and self.q1safe():
                    self.lastStep = self.getRelativeDirection(Direction.RIGHT)

                else:
                    print("no case has been found ===================================")
                    self.state = "survive"
                    return self.survive()

                if self.lastStep == self.getRelativeDirection(Direction.RIGHT):
                    if (
                        self.lastStep == Direction.UP and
                        self.mapObj.map[29 - self.mapObj.look(Direction.UP)][45].ignore and
                        self.mapObj.look(Direction.RIGHT) > 0
                    ):
                            self.lastStep = Direction.RIGHT
                    elif (
                        self.lastStep == Direction.RIGHT and
                        self.mapObj.map[30][46 + self.mapObj.look(Direction.RIGHT)].ignore and
                        self.mapObj.look(Direction.DOWN) > 0
                    ):
                        self.lastStep = Direction.DOWN
                    elif (
                        self.lastStep == Direction.LEFT and
                        self.mapObj.map[30][44 - self.mapObj.look(Direction.LEFT)].ignore and
                        self.mapObj.look(Direction.UP) > 0
                    ):
                        self.lastStep = Direction.UP
                    elif (
                        self.lastStep == Direction.DOWN and
                        self.mapObj.map[31 + self.mapObj.look(Direction.DOWN)].ignore and
                        self.mapObj.look(Direction.LEFT) > 0
                    ):
                        self.lastStep = Direction.LEFT

            return self.lastStep


    # TODO: Circle original pos stepper
    def circlePosStepper(self):
        if self.lastStep == Direction.UP:
            self.huntStartPos[0] += 1
            if self.huntStartPos[0] == 60:
                self.huntStartPos[0] = 0

        elif self.lastStep == Direction.LEFT:
            self.huntStartPos[1] += 1
            if self.huntStartPos[1] == 90:
                self.huntStartPos[1] = 0

        elif self.lastStep == Direction.RIGHT:
            self.huntStartPos[1] -= 1
            if self.huntStartPos[1] == -1:
                self.huntStartPos[1] = 89

        elif self.lastStep == Direction.DOWN:
            self.huntStartPos[0] -= 1
            if self.huntStartPos[0] == -1:
                self.huntStartPos[0] = 59

    def getTargetCellDirection(self) -> Direction:
        for i in range(60):
            for j in range(90):
                if self.mapObj.map[i][j] is self.targetCell:
                    self.targetCell.updateRPos(i, j)

        if abs(self.targetCell.rPosX) > abs(self.targetCell.rPosY):
            if self.targetCell.rPosX > 0:
                return Direction.RIGHT
            else:
                return Direction.LEFT

        elif abs(self.targetCell.rPosY) > abs(self.targetCell.rPosX):
            if self.targetCell.rPosY > 0:
                return Direction.UP
            else:
                return Direction.DOWN

        else:
            if self.targetCell.rPosX > 0:
                return Direction.RIGHT
            else:
                return Direction.LEFT

    # TODO: Survive mode: <=============================================================================================
    def survive(self):
        #print("Called 'survive' mode")
        return self.lastStep

    # Descriptions of all of these modes can be found in the get_next_direction
    #  method, in the section labeled "Mode Callers".

    # TODO: getRelativeDirection()
    # Returns input direction relative to the snek
    # - UP = FORWARD
    # - DOWN = BACKWARD
    def getRelativeDirection(self, directIn: Direction, lastStep = None) -> Direction:
        if lastStep is None:
            lastStep = self.lastStep

        if lastStep == Direction.UP:
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

        elif lastStep == Direction.LEFT:
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

        elif lastStep == Direction.RIGHT:
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

        elif lastStep == Direction.DOWN:
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
            raise ValueError("Invalid direction")


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
                    return True

                # ditto
                elif direction == Direction.LEFT:
                    self.map[30][45 - distance].occupied = True
                    return True

                # ditto
                elif direction == Direction.RIGHT:
                    self.map[30][45 + distance].occupied = True
                    return True

                # ditto
                elif direction == Direction.DOWN:
                    self.map[30 + distance][45].occupied = True
                    return True
                else:
                    raise ValueError("Invalid direction")


        def fillHead(self):
            # Set cell where snek's head is to be occupied
            self.map[30][45].occupied = True
            self.map[30][45].ignore = True


        def look(self, direction: Direction):
            i = 0
            if direction == Direction.UP:
                while True:
                    if self.map[29 - i][45].occupied:
                        break
                    if i >= 19:
                        break
                    i += 1

            elif direction == Direction.LEFT:
                while True:
                    if self.map[30][44 - i].occupied:
                        break
                    if i >= 19:
                        break
                    i += 1

            elif direction == Direction.RIGHT:
                while True:
                    if self.map[30][46 + i].occupied:
                        break
                    if i >= 19:
                        break
                    i += 1

            else:
                while True:
                    if self.map[31 + i][45].occupied:
                        break
                    if i >= 19:
                        break
                    i += 1

            return i



        def updateAccess(self):
            for y in range(1, 59):
                for x in range(1, 89):
                    if not self.map[y][x].occupied:
                        currentCell = self.map[y][x]
                        occupiedCounter = 0
                        ignoreCounter = 0

                        if self.map[y - 1][x].occupied:
                            occupiedCounter += 1
                            if self.map[y - 1][x].ignore:
                                ignoreCounter += 1

                        if self.map[y + 1][x].occupied:
                            occupiedCounter += 1
                            if self.map[y + 1][x].occupied:
                                ignoreCounter += 1
                        if self.map[y][x - 1].occupied:
                            occupiedCounter += 1
                            if self.map[y][x - 1].occupied:
                                ignoreCounter += 1
                        if self.map[y][x + 1].occupied:
                            occupiedCounter += 1
                            if self.map[y][x + 1].occupied:
                                ignoreCounter += 1

                        if occupiedCounter >= 3:
                            currentCell.occupied = True

                        if ignoreCounter >= 3:
                            currentCell.ignore = True


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
        for direction in Direction:
            self.mapObj.fillCell(direction, self.look(direction))


    # TODO: isSafe()
    def isSafe(self, direction) -> bool:
        if direction in self.dangerData:
            return False
        return True


    # TODO: Quarter safe checkers <=====================================================================================
    def q1safe(self):
        if self.lastStep == Direction.UP:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 - i][45 + j].occupied:
                        return False

        elif self.lastStep == Direction.LEFT:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 - i][45 - j].occupied:
                        return False

        elif self.lastStep == Direction.RIGHT:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 + i][45 + j].occupied:
                        return False

        elif self.lastStep == Direction.DOWN:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 + i][45 - j].occupied:
                        return False

        return True


    def q2safe(self):
        if self.lastStep == Direction.UP:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 - i][45 - j].occupied:
                        return False

        elif self.lastStep == Direction.LEFT:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 + i][45 - j].occupied:
                        return False

        elif self.lastStep == Direction.RIGHT:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 - i][45 + j].occupied:
                        return False

        elif self.lastStep == Direction.DOWN:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 + i][45 + j].occupied:
                        return False

        return True


    def q3safe(self):
        if self.lastStep == Direction.UP:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 + i][45 - j].occupied:
                        return False

        elif self.lastStep == Direction.LEFT:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 + i][45 + j].occupied:
                        return False

        elif self.lastStep == Direction.RIGHT:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 - i][45 - j].occupied:
                        return False

        elif self.lastStep == Direction.DOWN:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 - i][45 + j].occupied:
                        return False

        return True


    def q4safe(self):
        if self.lastStep == Direction.UP:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 + i][45 + j].occupied:
                        return False

        elif self.lastStep == Direction.LEFT:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 - i][45 + j].occupied:
                        return False

        elif self.lastStep == Direction.RIGHT:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 + i][45 - j].occupied:
                        return False

        elif self.lastStep == Direction.DOWN:
            for i in range(1, 3):
                for j in range(1, 3):
                    if i == j and i == 0:
                        continue
                    elif self.mapObj.map[30 - i][45 - j].occupied:
                        return False

        return True


    def forwardSafe(self):
        if self.mapObj.look(self.getRelativeDirection(Direction.UP)) < 2:
            return False
        return True

    def leftSafe(self):
        if self.mapObj.look(self.getRelativeDirection(Direction.LEFT)) < 2:
            return False
        return True

    def rightSafe(self):
        if self.mapObj.look(self.getRelativeDirection(Direction.RIGHT)) < 2:
            return False
        return True

    def backwardSafe(self):
        return False
        # look... don't judge me I thought this was hilarious.


# TODO: Bottom c:
