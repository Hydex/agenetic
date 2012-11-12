#!/usr/bin/env python

# Copyright (c) 2012, Nick Harvey
# All rights reserved.

# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# - Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice, 
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of the <ORGANIZATION> nor the names of its contributors
#   may be used to endorse or promote products derived from this software 
#   without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.



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