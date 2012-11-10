import random, sys

class Matrix:

	def __init__(self):
		self.width = 1
		self.height = 1
		self.values = []

	def setWidth(self, width):
		if (width >= 1):
			self.width = int(width)
		else:
			throw("Unable to set the width of a matrix to 0 or less")
		return self

	def setHeight(self, height):
		if (height >= 1):
			self.height = int(height)
		else:
			throw("Unable to set the height of a matrix to 0 or less")
		return self
	
	def getWidth(self):
		return self.width
	def getHeight(self):
		return self.height

	def init(self, fillValue = 0):
		for i in range(self.height):
			row = [fillValue for w in range(self.width)];
			self.values.append(row)
		return self

	def randomFill(self, min, max):
		lmin = min * 1000;
		lmax = max * 1000;
		for i in range(self.height):
			row = [];
			for j in range(self.width):
				row.append(random.random()*(lmax-lmin)+lmin)
			self.values.append(row)
		return self
	
	def getElem(self, row, col):
		return self.values[row][col]

	def setElem(self, row, col, value):
		self.values[row][col] = value
		return self
	
	def multiply(self, two, one):
		acc = 0
		res = Matrix()
		# print(one.getWidth(), one.getHeight(), two.getWidth(), two.getHeight())
		if (one.getWidth() != two.getHeight()):
			print("Matrices must have compatible sizes", one.getWidth(), two.getHeight());
			sys.exit()
		
		res.setWidth(two.getWidth()).setHeight(one.getHeight()).init();
		
		for i in range(one.getHeight()):  ## loop over left hand rows
			for j in range(two.getWidth()):  ## loop over the right hand columns
				acc = 0
				for k in range(one.getWidth()):  ## loop over each element pair and sum multiplicands
					acc += (one.getElem(i, k) * two.getElem(k, j))
				res.setElem(i, j, acc)
		# print(one.getWidth(), one.getHeight(), two.getWidth(), two.getHeight(), res.getWidth(), res.getHeight())
		return res
	
	def divide(self, divisor):
		for i in range(self.height):
			for j in range(self.width):
				self.setElem(i, j, self.getElem(i, j) / divisor)
		return self
	
	def render(self, color="black"):
		out = "<table>"
		for i in range(self.height):
			out += "<tr>"
			for j in range(self.width):
				out += "<td";
				style = "color: "+color
				if (j == 1): style += ";border-left: 1px solid black"
				if (j == self.width): style += ";border-right: 1px solid black"
				out += " style='"+style+"'>"+str(self.getElem(i, j))+"</td>"
			out += "</tr>"

		out += "</table>"
		return out

	def renderT(self, color="black"):
		out = ""
		for i in range(self.height):
			out += "| "
			for j in range(self.width):
				out += str(self.getElem(i, j))
			out += " |\n"
		return out

	def copy(self):
		res = Matrix()
		res.setWidth(self.getWidth()).setHeight(self.getHeight()).init();
		for i in range(self.getHeight()):  ## loop over left hand rows
			for j in range(self.getWidth()):  ## loop over the right hand columns
				res.setElem(i, j, self.getElem(i, j))
		return res		