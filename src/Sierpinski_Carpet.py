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

def drawSquare(points, myTurtle):
	# points: vec2[2], defines the bounding box of the square (top left corner, bottom right corner)

	# main directions
	myTurtle.up() # Pen up
	myTurtle.goto(points[0][0], points[0][1]) # top left

	myTurtle.down() # Pen down
	myTurtle.goto(points[1][0], points[0][1]) # top right
	myTurtle.goto(points[1][0], points[1][1]) # bottom right
	myTurtle.goto(points[0][0], points[1][1]) # bottom left
	myTurtle.goto(points[0][0], points[0][1]) # top left

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

def sierpinski_sq(points, degree, myTurtle):
	# draw a square based on the 3 points given
	color = getDegreeColor(degree)

	# begin fill
	myTurtle.fillcolor(color) # set color
	myTurtle.begin_fill()

	drawSquare(points, myTurtle)

	# end fill
	myTurtle.end_fill()

	if degree > 0:
		step_x = round((points[1][0] -points[0][0]) /3) # go with multiples of 3 for bounding box
		step_y = round((points[1][1] -points[0][1]) /3)
		offset_x = 0
		offset_y = 0
		pos_y = points[0][1] +step_y
		for i in range(8):
			if i <= 2:
				sierpinski_sq([[points[0][0] +offset_x, points[0][1]], [points[0][0] +offset_x +step_x, pos_y]], degree -1, myTurtle)
				if i < 2:
					offset_x += step_x
			elif i == 3:
				sierpinski_sq([[points[0][0] +offset_x, pos_y], [points[0][0] +offset_x +step_x, pos_y +step_y]], degree -1, myTurtle)
				pos_y += step_y *2 # floor of third row
			elif i <= 6:
				sierpinski_sq([[points[0][0] +offset_x, pos_y -step_y], [points[0][0] +offset_x +step_x, pos_y]], degree -1, myTurtle)
				offset_x -= step_x
			else:
				# last iteration
				sierpinski_sq([[points[0][0], pos_y -step_y *2], [points[0][0] +step_x, pos_y -step_y]], degree -1, myTurtle)

def main():
	myTurtle = turtle.Turtle()
	myTurtle.speed(10) # adjust the drawing speed here

	myWin = turtle.Screen()
	myWin.colormode(255)

	# 3 points of the first triangle based on [x,y] coordinates
	myPoints = [[-210, 210], [213, -213]]
	degree = 3 # Vary the degree of complexity here

	# first call of the recursive function
	sierpinski_sq(myPoints, degree, myTurtle)

	myTurtle.hideturtle() # hide the turtle cursor after drawing is

	# completed
	myWin.exitonclick() # Exit program when user click on window

main()