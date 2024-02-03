"""
CHONG CHENG HOCK
230643M
GROUP 01
"""
import turtle

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

def drawTriangle(points, myTurtle):
	myTurtle.up() # Pen up
	myTurtle.goto(points[0][0],points[0][1])
	myTurtle.down() # Pen down
	myTurtle.goto(points[1][0],points[1][1])
	myTurtle.goto(points[2][0],points[2][1])
	myTurtle.goto(points[0][0],points[0][1])

def getMid(p1,p2):
	return ((p1[0] + p2[0]) /2, (p1[1] + p2[1]) /2)

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


def sierpinski(points, degree, myTurtle):
	# draw a triangle based on the 3 points given
	color = getDegreeColor(degree) # get color based on degree

	# begin fill
	myTurtle.fillcolor(color) # set color
	myTurtle.begin_fill()

	# draw triangle
	drawTriangle(points, myTurtle)

	# end fill
	myTurtle.end_fill()

	if degree > 0:
		sierpinski([points[0], getMid(points[0], points[1]), getMid(points[0], points[2])],	degree-1, myTurtle)
		sierpinski([points[1], getMid(points[0], points[1]), getMid(points[1], points[2])], degree-1, myTurtle)
		sierpinski([points[2], getMid(points[2], points[1]), getMid(points[0], points[2])], degree-1, myTurtle)

def main():
	myTurtle = turtle.Turtle()
	myTurtle.speed(100) # adjust the drawing speed here
	myTurtle.hideturtle() # hide turtle, else shows up as an artifact in final render

	myWin = turtle.Screen()
	myWin.colormode(255)
	myWin.bgcolor(33, 33, 33)

	# 3 points of the first triangle based on [x,y] coordinates
	myPoints = [[-200,-50],[0,200],[200,-50]]
	degree = 6 # Vary the degree of complexity here

	# first call of the recursive function
	sierpinski(myPoints, degree, myTurtle)

	# completed
	myWin.exitonclick() # Exit program when user click on window

main()