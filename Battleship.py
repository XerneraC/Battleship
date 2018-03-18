import random


class array2D:
	def __init__(self, height, width, defaultValue=0):
		self.height = height
		self.width = width
		self.array = [defaultValue] * (height * width)

	def setValue(self, x, y, newValue):
		index = (y - 1) * self.width + (x - 1)
		self.array[index] = newValue

	def getValue(self, x, y):
		index = (y - 1) * self.width + (x - 1)
		return self.array[index]

	def print2D(self):
		print("    A B C D E F G H I J")
		print("    | | | | | | | | | |")
		for y in range(self.height):
			prntStr = (" " + str(y + 1) + "——") if y < 9 else (
			    str(y + 1) + "——")
			for x in range(self.width):
				index = y * self.width + x
				value = self.array[index]
				if value == 0:
					prntStr = prntStr + "  "
				elif value == 1:
					prntStr = prntStr + "O "
				elif value == 2:
					prntStr = prntStr + "X "
				elif value == 3:
					prntStr = prntStr + "1 "
				elif value == 4:
					prntStr = prntStr + "2 "
				elif value == 5:
					prntStr = prntStr + "3 "
				elif value == 6:
					prntStr = prntStr + "4 "
				else:
					prntStr = prntStr + str(self.array[index]) + " "
			print(prntStr[:-1])


def getCoordinate(coordinate):
	xValues = {
	    "A": 1,
	    "B": 2,
	    "C": 3,
	    "D": 4,
	    "E": 5,
	    "F": 6,
	    "G": 7,
	    "H": 8,
	    "I": 9,
	    "J": 10,
	}
	if coordinate[0] in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
		x = xValues[coordinate[0]]
		y = int(coordinate[1:])
		return x, y
	else:
		print("You tried to play smart didn't you? Well I can play smart too and just stop running!")
		exit()


class player:
	def __init__(self):
		self.ownSea = array2D(10, 10)
		self.oponentSea = array2D(10, 10)
		
		self.numberOfShips = {
			1: 0,
			2: 0,
			3: 0,
			4: 0
		}

	def checkHit(self, coordinate):
		x = 0
		y = 0
		x, y = getCoordinate(coordinate)
		isHit = self.ownSea.getValue(x, y) in [3, 4, 5, 6]
		if isHit:
			self.ownSea.setValue(x, y, 2)
		else:
			self.ownSea.setValue(x, y, 1)
		return isHit

	def attackOponent(self, oponent, coordinate):
		isHit = oponent.checkHit(coordinate)
		x = 0
		y = 0
		x, y = getCoordinate(coordinate)
		if isHit:
			self.oponentSea.setValue(x, y, 2)
		else:
			self.oponentSea.setValue(x, y, 1)
		return isHit

	def printPlayer(self):
		print("Your Oponent's Sea:")
		self.oponentSea.print2D()
		print("")
		print("Your Sea:")
		self.ownSea.print2D()

	def placeShip(self, x, y, rotation, shipClass):
		# Ship Classes:
		# 1: 2 long (4x)
		# 2: 3 long (3x)
		# 3: 4 long (2x)
		# 4: 6 long (1x)
		#
		# rotation:
		# 0: right
		# 1: down
		# 2: left
		# 3: up

		shipLenghts = {
			1: 2,
			2: 3,
			3: 4,
			4: 6
		}
		
		maxShips = {
			1: 4,
			2: 3,
			3: 2,
			4: 1
		}
		
		def checkCoordinate(x, y):
			isPossible = True
			if x > 10:
				isPossible = False
			if y > 10:
				isPossible = False
			if x < 1:
				isPossible = False
			if y < 1:
				isPossible = False
			if isPossible:
				if self.ownSea.getValue(x, y) in [3, 4, 5, 6]:
					isPossible = False
			return isPossible
		
		wasPlaced = False
		if self.numberOfShips[shipClass] < maxShips[shipClass]:
			tempX = x
			tempY = y
			isShipPossible = True
			for _ in range(shipLenghts[shipClass]):
				if not(checkCoordinate(tempX, tempY)):
					isShipPossible = False
				if rotation == 0:
					tempX += 1
				if rotation == 1:
					tempY += 1
				if rotation == 2:
					tempX -= 1
				if rotation == 3:
					tempY -= 1
			
			if isShipPossible:
				self.numberOfShips[shipClass] += 1
				wasPlaced = True
				tempX = x
				tempY = y
				for square in range(shipLenghts[shipClass]):
					self.ownSea.setValue(tempX, tempY, shipClass + 2)
					if rotation == 0:
						tempX += 1
					if rotation == 1:
						tempY += 1
					if rotation == 2:
						tempX -= 1
					if rotation == 3:
						tempY -= 1
		return wasPlaced
	
	def placeRandomShip(self, shipClass):
		while True:
			x = random.randint(1, 10)
			y = random.randint(1, 10)
			rot = random.randint(0,3)
			wasPlaced = self.placeShip(x, y, rot, shipClass)
			if wasPlaced:
				break
	
	def populate(self):
		
		self.placeRandomShip(4)
		
		self.placeRandomShip(3)
		self.placeRandomShip(3)
		
		self.placeRandomShip(2)
		self.placeRandomShip(2)
		self.placeRandomShip(2)
		
		self.placeRandomShip(1)
		self.placeRandomShip(1)
		self.placeRandomShip(1)
		self.placeRandomShip(1)


def isDead(player):
	isDead = True
	for square in player.ownSea.array:
		if square in [3, 4, 5, 6]:
			isDead = False
	return isDead


player1 = player()
player2 = player()

player1.populate()
player2.populate()

while True:
	ok1 = input("It's Player 1's turn. Type 'ok' if you're ready:").upper()
	if ok1 == "OK":
		print("Nice!")
	else:
		print("Close enough...")
	
	print("")
	player1.printPlayer()
	print("")
	move1 = input("Where will you shoot?").upper()
	print("")
	if move1 == "1941":
		print("YOU HAVE CALLED UPON PEARL HARBOR! THE ENEMY SHALL BE PUNISHED BY HAVING EVERY SQUARE OF THEIR SEA BOMBARDED!")
		for x in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
			for y in range(10):
				player1.attackOponent(player2, (x + str(y+1)))
	else:
		isHit = player1.attackOponent(player2, move1)
		print("Targeting " + move1 + "!")
		print("It was a hit!" if isHit else "It was a miss!")
	
	print("")
	
	isP1Winner = isDead(player2)
	if isP1Winner:
		print("Player 1 Wins!")
		break
	
	input("Press enter to continue...")
	
	print("")
		
	for _ in range(100):
		print("")
	
	print("")
	
	
	
	ok2 = input("It's Player 2's turn. Type 'ok' if you're ready:").upper()
	if ok2 == "OK":
		print("Nice!")
	else:
		print("Close enough...")
	
	print("")
	player2.printPlayer()
	print("")
	move2 = input("Where will you shoot?").upper()
	print("")
	if move2 == "1941":
		print("YOU HAVE CALLED UPON PEARL HARBOR! THE ENEMY SHALL BE PUNISHED BY HAVING EVERY SQUARE OF THEIR SEA BOMBARDED!")
		for x in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
			for y in range(10):
				player1.attackOponent(player1, (x + str(y+1)))
	else:
		isHit = player2.attackOponent(player1, move1)
		print("Targeting " + move2 + "!")
		print("It was a hit!" if isHit else "It was a miss!")
	
	print("")
	
	isP2Winner = isDead(player1)
	if isP2Winner:
		print("Player 2 Wins!")
		break
	
	input("Press enter to continue...")
	
	print("")
		
	for _ in range(100):
		print("")
	
	print("")
