"""
CHONG CHENG HOCK
230643M
GROUP 01
"""
import turtle
import math

# constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

COLOR_MAP = [
	(42, 38, 130),
	(69, 32, 128),
	(90, 24, 125),
	(108, 9, 121),
	(124, 0, 114),
	(139, 0, 107),
	(151, 0, 98),
	(162, 0, 89),
	(171, 0, 78),
	(178, 0, 68),
	(184, 0, 56),
	(188, 0, 44),
	(190, 0, 31),
	(190, 14, 14)
]

class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	@property
	def magnitude(self):
		"""
		returns the magnitude of a vector as a float
		"""
		return (self.x **2 +self.y **2) **.5

	def unit(self):
		"""
		returns a new unit vector based from self
		"""
		mag = self.magnitude
		return Vector2(self.x /mag, self.y /mag)

	def rotate(self, alpha):
		"""
		alpha: radians to rotate anti-clockwise

		rotates a vector anti-clockwise by alpha via rotation matrix
		returns a directional vector with the same magnitude as itself
		"""
		cosa = math.cos(alpha)
		sina = math.sin(alpha)

		return Vector2(self.x *cosa -self.y *sina, self.x *sina +self.y *cosa)

	def lhPerpendicular(self):
		"""
		returns a unit vector that is perpendicular on the left hand side
		"""
		return Vector2(-self.y, self.x).unit()

	def draw(self, origin, myTurtle):
		"""
		origin: vector2
		turtle: turtle object

		draws a line to self from origin with turtle (vector = self -origin)
		"""
		myTurtle.up()
		myTurtle.goto(origin.x, origin.y)

		myTurtle.down()
		myTurtle.goto(self.x, self.y)

	def __add__(self, roperand):
		if (isinstance(roperand, Vector2)):
			return Vector2(self.x +roperand.x, self.y +roperand.y)
		else:
			return ValueError("Adding Vector2 with type", type(roperand))

	def __sub__(self, roperand):
		if (isinstance(roperand, Vector2)):
			return Vector2(self.x -roperand.x, self.y -roperand.y)
		else:
			return ValueError("Subtracting from Vector2 with type", type(roperand))

	def __mul__(self, roperand):
		"""
		returns new vector2 based on roperand
		"""
		if (type(roperand) == int or type(roperand) == float):
			return Vector2(self.x *roperand, self.y *roperand)
		elif (isinstance(roperand, Vector2)):
			return Vector2(self.x *roperand.x, self.y *roperand.y)
		else:
			raise ValueError("Multiplying Vector2 with type", type(roperand))

	def __repr__(self):
		"""
		for debugging
		"""
		return "<{}, {}>".format(self.x, self.y)

def getDegreeColor(degree):
	"""
	degrees is descending, i.e. starts from a high number
	essentially return a color that repeats the COLOR_MAP with reversal if degree exceeds range (e.g. [0, 1, 2, 3, 2, 1, 0, 1, ...])

	return a tuple (r, g, b) from COLOR_MAP mapped by degree with reverse order
	"""
	b = len(COLOR_MAP) # boundaries
	idx = degree
	if (degree >= b):
		i = degree -b
		j = i //(b -1)
		k = i % (b -1)
		if (j % 2 == 0):
			# even
			idx = b -k -2 # descending mapping
		else:
			# odd
			idx = 1 + k # ascending mapping

	return COLOR_MAP[idx]


# START OF BUILDING BLOCK FUNCTION #
def drawSquare(myTurtle, origin, perpendicularBaseVector):
	"""
	origin: vector2
	perpendicularBaseVector: vector2, base directional vector (left to right)

	draws a square starting from origin, lb to rb, rb to rt, rt to lt, lt to lb (left bottom)
	size of square depends on magnitude of perpendicularBaseVector
	baseVector also determines 'tilt' of square

	returns the four points in sequence [bottom left, bottom right, top right, top left]
	"""
	directional = perpendicularBaseVector
	points = [] # to be build
	for i in range(4):
		points.append(origin)
		(origin +directional).draw(origin, myTurtle)
		origin += directional # absolute x, y end coordinates

		if (i < 3):
			# do not rotate on the last iteration (not needed)
			directional = directional.rotate(math.pi /2)

	return points

def drawInnerDesign(myTurtle, points):
	for i in range(0, len(points), 2):
		j = i +2
		if (j >= len(points)):
			j -= 6
		points[i].draw(points[j], myTurtle)

	if (len(points) % 2 == 0):
		# even
		points[0].draw(points[len(points) -2], myTurtle)

def drawNgon(myTurtle, origin, perpendicularBaseVector, n):
	"""
	origin: vector2
	perpendicularBaseVector: vector2, base directional vector (left to right)

	draws a polygon with n-sides

	returns points in order starting from origin
	"""
	directional = perpendicularBaseVector
	points = [] # to be build
	angle = math.pi *2 /n # radians
	for i in range(n):
		points.append(origin)
		(origin +directional).draw(origin, myTurtle)
		origin += directional # absolute x, y end coordinates

		if (i < n -1):
			# do not rotate on the last iteration (to be returned)
			directional = directional.rotate(angle)

	return points

def drawIsosTriangle(myTurtle, origin, perpendicularBaseVector):
	"""
	draws isoceles triangle

	returns the three points in sequence [bottom left, bottom right, apex]
	"""
	points = [origin] # to be build
	directional = perpendicularBaseVector # base directional vector
	(origin +directional).draw(origin, myTurtle)
	origin += directional
	points.append(origin) # right bottom

	# draw right side of triangle
	# from cos(45deg) = sqrt(2) /2
	# thus, length of isos triangle side = (baseLength /2) /(cos(45deg))
	directional = directional.rotate(math.pi *3/4) # rotate direction vector by supplemnetary angle (180 - 60)deg to form convex insides of triangle
	apexDirectional = directional.unit() *(directional.magnitude /math.sqrt(2)) # length of isos triangle side
	(origin +apexDirectional).draw(origin, myTurtle)
	origin += apexDirectional
	points.append(origin) # apex point

	directional = apexDirectional.rotate(math.pi /2) # same length as apexDirectional vector (both sides of the isosceles triangle have the same length)
	(origin +directional).draw(origin, myTurtle)

	return points

def drawLeftLeanRightTriangle(myTurtle, origin, perpendicularBaseVector):
	"""
	draws right angled triangle leans towards the left

	returns the three points in sequence [bottom left, bottom right, apex]
	"""
	points = [origin] # to be build

	directional = perpendicularBaseVector # base directional vector
	(origin +directional).draw(origin, myTurtle)
	origin += directional
	points.append(origin) # right bottom2

	# draw right side of triangle
	# length of height of triangle side = cos(55deg) *baseLength
	directional = directional.rotate(math.pi *25/36) # rotate direction vector by supplemnetary angle (180 - 55)deg to form convex insides of triangle
	apexDirectional = directional.unit() *(math.cos(math.pi *11/36) *perpendicularBaseVector.magnitude) # length of side of triangle by trig ratios
	(origin +apexDirectional).draw(origin, myTurtle)
	origin += apexDirectional
	points.append(origin) # apex point

	directional = apexDirectional.rotate(math.pi /2) # from apex back to origin
	apexDirectionalDown = directional.unit() *(math.sin(math.pi *11/36) *perpendicularBaseVector.magnitude) # length of side of triangle by trig ratios using the same angle
	(origin +apexDirectionalDown).draw(origin, myTurtle)

	return points

def drawRightLeanRightTriangle(myTurtle, origin, perpendicularBaseVector):
	"""
	draws right angled triangle leans towards the right

	returns the three points in sequence [bottom left, bottom right, apex]
	"""
	points = [origin] # to be build

	directional = perpendicularBaseVector # base directional vector
	(origin +directional).draw(origin, myTurtle)
	origin += directional
	points.append(origin) # right bottom

	# draw right side of triangle
	# length of height of triangle side = cos(35deg) *baseLength
	directional = directional.rotate(math.pi *29/36) # rotate direction vector by supplemnetary angle (180 - 35)deg to form convex insides of triangle
	apexDirectional = directional.unit() *(math.cos(math.pi *7/36) *perpendicularBaseVector.magnitude) # length of side of triangle by trig ratios
	(origin +apexDirectional).draw(origin, myTurtle)
	origin += apexDirectional
	points.append(origin) # apex point

	directional = apexDirectional.rotate(math.pi /2) # from apex back to origin
	apexDirectionalDown = directional.unit() *(math.sin(math.pi *7/36) *perpendicularBaseVector.magnitude) # length of side of triangle by trig ratios using the same angle
	(origin +apexDirectionalDown).draw(origin, myTurtle)

	return points
# END OF BUILDING BLOCK FUNCTION #


# START OF COMPONENT BUILDING FUNCTIONS #
def drawBalancedComponent(myTurtle, origin, baseDirectionalVector, fillcolor):
	"""
	draws a balanced component (square + isosceles triangle) of the pythagoras' tree

	returns a pair of coordinates (origin, directionalVector) where origin is the start of the new branch component and directionalVector is to be used as the base directional vector to build the new branch component
	"""
	myTurtle.fillcolor(*fillcolor)

	myTurtle.begin_fill()
	sqPoints = drawNgon(myTurtle, origin, baseDirectionalVector, 12)
	myTurtle.end_fill()

	myTurtle.begin_fill()
	isosPoints = drawIsosTriangle(myTurtle, sqPoints[7], sqPoints[6] -sqPoints[7]) # use point 7 on dodecagon (left corner of top flat side) as origin for triangle since directional would go left to right
	myTurtle.end_fill()

	drawInnerDesign(myTurtle, sqPoints)

	return [
		(sqPoints[7], isosPoints[2] -isosPoints[0]),
		(isosPoints[2], isosPoints[1] -isosPoints[2])
	]

def drawLeftLeanComponent(myTurtle, origin, baseDirectionalVector, fillcolor):
	"""
	draws a left leaning component (square + left lean right-angle triangle) of the pythagoras' tree

	returns a pair of coordinates (origin, directionalVector) where origin is the start of the new branch component and directionalVector is to be used as the base directional vector to build the new branch component
	"""
	myTurtle.fillcolor(*fillcolor)

	myTurtle.begin_fill()
	sqPoints = drawNgon(myTurtle, origin, baseDirectionalVector, 8)
	myTurtle.end_fill()

	myTurtle.begin_fill()
	isosPoints = drawLeftLeanRightTriangle(myTurtle, sqPoints[5], sqPoints[4] -sqPoints[5])
	myTurtle.end_fill()

	drawInnerDesign(myTurtle, sqPoints)

	return [
		(sqPoints[5], isosPoints[2] -isosPoints[0]),
		(isosPoints[2], isosPoints[1] -isosPoints[2])
	]

def drawRightLeanComponent(myTurtle, origin, baseDirectionalVector, fillcolor):
	"""
	draws a right leaning component (square + right lean right-angle triangle) of the pythagoras' tree

	returns a pair of coordinates (origin, directionalVector) where origin is the start of the new branch component and directionalVector is to be used as the base directional vector to build the new branch component
	"""
	myTurtle.fillcolor(*fillcolor)

	myTurtle.begin_fill()
	sqPoints = drawNgon(myTurtle, origin, baseDirectionalVector, 8)
	myTurtle.end_fill()

	myTurtle.begin_fill()
	isosPoints = drawRightLeanRightTriangle(myTurtle, sqPoints[5], sqPoints[4] -sqPoints[5])
	myTurtle.end_fill()

	drawInnerDesign(myTurtle, sqPoints)

	return [
		(sqPoints[5], isosPoints[2] -isosPoints[0]),
		(isosPoints[2], isosPoints[1] -isosPoints[2])
	]
# END OF COMPONENT BUILDING FUNCTIONS #



# START OF MASTER BUILDING FUNCTION #
def balancedPythagorasTree(myTurtle, origin, baseDirectionalVector, degree):
	# draw component (base square + triangle)
	color = getDegreeColor(degree)
	left, right = drawBalancedComponent(myTurtle, origin, baseDirectionalVector, color)
	if degree > 0:
		# recursive case
		balancedPythagorasTree(myTurtle, left[0], left[1], degree -1)
		balancedPythagorasTree(myTurtle, right[0], right[1], degree -1)

def leftLeanPythagorasTree(myTurtle, origin, baseDirectionalVector, degree):
	# draw component (base square + triangle)
	color = getDegreeColor(degree)
	left, right = drawLeftLeanComponent(myTurtle, origin, baseDirectionalVector, color)
	if degree > 0:
		# recursive case
		leftLeanPythagorasTree(myTurtle, left[0], left[1], degree -1)
		leftLeanPythagorasTree(myTurtle, right[0], right[1], degree -1)

def rightLeanPythagorasTree(myTurtle, origin, baseDirectionalVector, degree):
	# draw component (base square + triangle)
	color = getDegreeColor(degree)
	left, right = drawRightLeanComponent(myTurtle, origin, baseDirectionalVector, color)
	if degree > 0:
		# recursive case
		rightLeanPythagorasTree(myTurtle, left[0], left[1], degree -1)
		rightLeanPythagorasTree(myTurtle, right[0], right[1], degree -1)
# START OF MASTER BUILDING FUNCTION #



def main():
	# turtle config
	myTurtle = turtle.Turtle()
	myTurtle.speed(100) # adjust the drawing speed here
	myTurtle.hideturtle() # hide turtle, else shows up as an artifact in final render

	# screen config
	myWin = turtle.Screen()
	myWin.colormode(255)
	myWin.bgcolor(33, 33, 33)
	myWin.setup(WINDOW_WIDTH, WINDOW_HEIGHT) # canvas dimensions
	myWin.tracer(0)

	# variable
	length = 65 # length of 1 side of the polygon in units

	#### UNCOMMENT THE FOLLOWING LINE: balanced
	balancedPythagorasTree(myTurtle, Vector2(length /-2, WINDOW_HEIGHT /-2 +10), Vector2(length, 0), 5)

	#### UNCOMMENT THE FOLLOWING LINE: left leaning
	# leftLeanPythagorasTree(myTurtle, Vector2(length /-2, WINDOW_HEIGHT /-2 +10), Vector2(length, 0), 5)

	#### UNCOMMENT THE FOLLOWING LINE: right leaning
	# rightLeanPythagorasTree(myTurtle, Vector2(length /-2, WINDOW_HEIGHT /-2 +10), Vector2(length, 0), 5)

	# exit on click
	myWin.exitonclick()

main()