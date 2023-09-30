import turtle
import random

t = turtle.Turtle()
t.penup()

t.speed(0)
t.hideturtle()
turtle.tracer(0, 0)

WORLD_WIDTH = 71
WORLD_HEIGHT = 71

WORLD_OFFSET = [-100, -100]

PIXEL_SIZE = 5

squareValues = []


def populate2DArray():

	worldMap = []

	for x in range(WORLD_WIDTH):
		xGrid = []
		for y in range(WORLD_HEIGHT):
			if x % (WORLD_WIDTH - 1) == 0 or y % (WORLD_HEIGHT - 1) == 0:
				xGrid.append(1)
			elif x % 2 == 0 and y % 2 == 0:
				xGrid.append(1)
			elif x % 2 == 1 and y % 2 == 0:
				xGrid.append(max(0, random.randint(0, 2) - 1))
			elif x % 2 == 0 and y % 2 == 1:
				xGrid.append(max(0, random.randint(0, 2) - 1))
			else:
				xGrid.append(0)

		worldMap.append(xGrid)

	return worldMap


def renderWorld(worldMap):
	for x in range(WORLD_WIDTH):
		for y in range(WORLD_HEIGHT):
			# Draw square at position

			if (worldMap[x][y] == 0):
				drawSquare(x, y, "#ffffff")
			else:
				drawSquare(x, y, "#000000")

	# Draw end square
	drawSquare(WORLD_WIDTH - 2, WORLD_HEIGHT - 2, "#22ff22")
	turtle.update()

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def drawSquare(x, y, colour):
	t.color(colour)
	t.fillcolor(colour)

	t.goto((x * PIXEL_SIZE) + WORLD_OFFSET[0], (y * PIXEL_SIZE) + WORLD_OFFSET[1])
	t.pendown()

	t.begin_fill()
	t.goto((x * PIXEL_SIZE) + PIXEL_SIZE + WORLD_OFFSET[0],
	       (y * PIXEL_SIZE) + WORLD_OFFSET[1])
	t.goto((x * PIXEL_SIZE) + PIXEL_SIZE + WORLD_OFFSET[0],
	       (y * PIXEL_SIZE) + PIXEL_SIZE + WORLD_OFFSET[1])
	t.goto((x * PIXEL_SIZE) + WORLD_OFFSET[0],
	       (y * PIXEL_SIZE) + PIXEL_SIZE + WORLD_OFFSET[1])
	t.goto((x * PIXEL_SIZE) + WORLD_OFFSET[0], (y * PIXEL_SIZE) + WORLD_OFFSET[1])
	t.end_fill()
	t.penup()


def setupMazeSolvingList():
	returnData = []
	for x in range(WORLD_WIDTH):
		widthList = []
		for y in range(WORLD_HEIGHT):
			widthList.append(99999999)

		returnData.append(widthList)

	return returnData


endPoints = []
endPoints.append([1, 1])

squareValues = setupMazeSolvingList()
squareValues[1][1] = 0

dist = 0

hasFoundEnd = False


def tracePath(xPos, yPos, maxDist, worldMap):
	global hasFoundEnd

	hasFoundEnd = True

	# Draw path back to start

	hasTracedPath = False

	currentPos = [xPos, yPos]
	currentDist = maxDist

	while not hasTracedPath:
		newPos = currentPos.copy()

		x = currentPos[0] - 1
		y = currentPos[1]

		if x >= 0:
			if worldMap[x][y] == 0 and squareValues[x][y] < currentDist:
				newPos = [x, y]
				currentDist = squareValues[x][y]

		x = currentPos[0]
		y = currentPos[1] - 1

		if y >= 0:
			if worldMap[x][y] == 0 and squareValues[x][y] < currentDist:
				newPos = [x, y]
				currentDist = squareValues[x][y]

		x = currentPos[0] + 1
		y = currentPos[1]

		if x < WORLD_WIDTH:
			if worldMap[x][y] == 0 and squareValues[x][y] < currentDist:
				newPos = [x, y]
				currentDist = squareValues[x][y]

		x = currentPos[0]
		y = currentPos[1] + 1

		if y < WORLD_HEIGHT:
			if worldMap[x][y] == 0 and squareValues[x][y] < currentDist:
				newPos = [x, y]
				currentDist = squareValues[x][y]

		currentPos = newPos

		drawSquare(currentPos[0], currentPos[1], rgb2hex(min((currentDist * 2), 255), 255, min((currentDist * 2), 255)))
		turtle.update()

		if currentPos[0] == 1 and currentPos[1] == 1:
			# Finished tracing path
			hasTracedPath = True


def solveMaze(worldMap):
	global endPoints
	global squareValues
	global dist

	newData = []

	i = len(endPoints) - 1

	if hasFoundEnd:
		i = -1

	while i >= 0:
		# Look around at the 4 adjacent squares

		x = endPoints[i][0] - 1
		y = endPoints[i][1]

		squareColour = rgb2hex(min(dist * 2, 255), 10, 255 - min(dist * 2, 255))

		if x >= 0:
			if worldMap[x][y] == 0 and squareValues[x][y] == 99999999:
				newData.append([x, y, dist])
				# Draw path to screen
				drawSquare(x, y, squareColour)
				squareValues[x][y] = dist

		x = endPoints[i][0]
		y = endPoints[i][1] - 1

		if y >= 0:
			if worldMap[x][y] == 0 and squareValues[x][y] == 99999999:
				newData.append([x, y, dist])
				# Draw path to screen
				drawSquare(x, y, squareColour)
				squareValues[x][y] = dist

		x = endPoints[i][0] + 1
		y = endPoints[i][1]

		if x < WORLD_WIDTH:
			if worldMap[x][y] == 0 and squareValues[x][y] == 99999999:
				newData.append([x, y, dist])
				# Draw path to screen
				drawSquare(x, y, squareColour)
				squareValues[x][y] = dist

		x = endPoints[i][0]
		y = endPoints[i][1] + 1

		if y < WORLD_HEIGHT:
			if worldMap[x][y] == 0 and squareValues[x][y] == 99999999:
				newData.append([x, y, dist])
				# Draw path to screen
				drawSquare(x, y, squareColour)
				squareValues[x][y] = dist

		turtle.update()
		i -= 1

	endPoints = newData.copy()

	if not hasFoundEnd:
		for x in range(len(newData)):
			# Check if search is complete

			if newData[x][0] == WORLD_WIDTH - 2 and newData[x][1] == WORLD_HEIGHT - 2:
				tracePath(endPoints[x][0], endPoints[x][1], endPoints[x][2], worldMap)

	dist += 1


# Draw world data to screen

WORLD_DATA = populate2DArray()
renderWorld(WORLD_DATA)

for i in range(500):
	solveMaze(WORLD_DATA)
	turtle.update()
