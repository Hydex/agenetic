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



import Matrix, random, copy, sys

class ga:

	def __init__(self):
		self.population = []
		self.coeff_size = 0

	def seedGA(self, size, inSize, hiddenSize, outSize):
		'Creates a new set of matrices for the neural network'
		self.size = size
		self.inSize = inSize
		self.hiddenSize = hiddenSize
		self.outSize = outSize
		self.coeff_size = (inSize * hiddenSize) + hiddenSize + (hiddenSize * outSize) + outSize
		
		for i in range(size):
			matrices = {}
			matrices["first_weights"] = self.getWeights(inSize, hiddenSize)
			matrices["first_thresholds"] = self.getThresholds(hiddenSize)
			matrices["second_weights"] = self.getWeights(hiddenSize, outSize)
			matrices["second_thresholds"] = self.getThresholds(outSize)
			self.population.append(matrices)

	def getInputSize(self):
		return self.inSize
	def getHiddenSize(self):
		return self.hiddenSize
	def getOutputSize(self):
		return self.outSize

	def setGA2(self, population):
		self.population = population
		self.size = len(self.population)

	def setGA(self, population):
		self.population = population
		self.size = len(self.population)
		temp = population[0]
		self.inSize = temp["first_weights"].getWidth()
		self.hiddenSize = temp["first_thresholds"].getHeight()
		self.outSize = temp["second_weights"].getHeight()
		self.coeff_size = (self.inSize * self.hiddenSize) + self.hiddenSize + (self.hiddenSize * self.outSize) + self.outSize

	def getWeights(self, width, height):
		m = Matrix.Matrix()
		m.setWidth(width)
		m.setHeight(height)
		m.randomFill(0, 1)
		return m

	def getThresholds(self, height):
		m = Matrix.Matrix()
		m.setHeight(height)
		m.randomFill(0, 2)
		return m

	def getPopulation(self):
		return self.population

	def mateParents(self, firstParentId, secondParentId):
		parent1 = self.population[firstParentId]
		parent2 = self.population[secondParentId]
		selector = int(random.random() * self.coeff_size)
		children = [parent1.copy(), parent2.copy()]

		# print("selector:", selector, self.coeff_size)
		if selector < (self.inSize * self.hiddenSize):
			selector_row = int(selector/self.inSize)
			selector_col = selector % self.inSize
			crossover_loc = "first_weights"
			# print("Crossing first weights", selector, selector_row, selector_col)
		else:
			# child["first_weights"] = parent1["first_weights"].copy()
			selector = selector - (self.inSize * self.hiddenSize)
			if selector < self.hiddenSize:
				selector_row = selector
				selector_col = 0
				crossover_loc = "first_thresholds"
				# print("Crossing first thresholds", selector, selector_row, selector_col)
			else:
				# child["first_thresholds"] = parent1["first_thresholds"].copy()
				selector = selector - (self.hiddenSize)
				if selector < (self.hiddenSize * self.outSize):
					selector_row = int(selector/self.inSize)
					selector_col = selector % self.hiddenSize
					crossover_loc = "second_weights"
					# print("Crossing second weights", selector, selector_row, selector_col)
				else:
					# child["second_weights"] = parent1["second_weights"].copy()
					selector = selector - (self.hiddenSize * self.outSize)
					selector_row = selector
					selector_col = 0
					crossover_loc = "second_thresholds"
					# print("Crossing second thresholds", selector, selector_row, selector_col)

		children[0][crossover_loc] = self.crossOver(parent1[crossover_loc], parent2[crossover_loc], selector_row, selector_col)
		children[1][crossover_loc] = self.crossOver(parent1[crossover_loc], parent2[crossover_loc], selector_row, selector_col)

		# print(parent1)
		# print(parent2)
		# print(child)

		return children

	def crossOver(self, parent_one, parent_two, row, col):
		"""crossover determines which chromozones progress to the next population"""
		rows = parent_one.getHeight()
		cols = parent_one.getWidth()
		cross = row*rows + col
		m = Matrix.Matrix().setWidth(cols).setHeight(rows).init()
		for i in range(rows):
			for j in range(cols):
				if (i*rows+j) < cross:
					m.setElem(i, j, parent_one.getElem(i, j))
				else:
					m.setElem(i, j, parent_two.getElem(i, j))
		return m

	def mutatePopulation(self, survivors, mutationRate, crossOver):
		newPopulation = []
		mutations = [0 for i in range(4)]
		for matrices in survivors:
			# matrices = self.population[s]
			if random.random() < mutationRate:
				selector = int(random.random() * self.coeff_size)
				#print("selector:", selector, self.coeff_size)
				if selector < (self.inSize * self.hiddenSize):
					selector_row = int(selector/self.inSize)
					selector_col = selector % self.inSize
					try:
						matrices["first_weights"].setElem(selector_row, selector_col, random.random())
					except:
						print("Selector: ", selector)
						print("Width: ", matrices["first_weights"].getWidth(), self.inSize, len(matrices["first_weights"].getData()[0]))
						print("Height: ", matrices["first_weights"].getHeight(), self.hiddenSize, len(matrices["first_weights"].getData()))
						print("Problems with setElem...")
						print(selector_row, selector_col)
						sys.exit()
					# print("Mutation in first matrix", selector, selector_row, selector_col)
					mutations[0] += 1
				else:
					selector = selector - (self.inSize * self.hiddenSize)
					if selector < self.hiddenSize:
						currVal = matrices["first_thresholds"].getElem(selector, 0)
						currVal += (0.1 - random.random()*0.2)
						if currVal > 2:
							currVal = 2
						elif currVal < 0:
							currVal = 0
						matrices["first_thresholds"].setElem(selector, 0, currVal)
						mutations[1] += 1
						# print("Mutation in first threshold", selector)
						pass
					else:
						selector = selector - (self.hiddenSize)
						if selector < (self.hiddenSize * self.outSize):
							selector_row = int(selector/self.inSize)
							selector_col = selector % self.hiddenSize
							matrices["second_weights"].setElem(selector_row, selector_col, random.random())
							mutations[2] += 1
							# print("Mutation in second matrix", selector, selector_row, selector_col)
						else:
							selector = selector - (self.hiddenSize * self.outSize)
							currVal = matrices["second_thresholds"].getElem(selector, 0)
							currVal += (0.1 - random.random()*0.2)
							if currVal > 2:
								currVal = 2
							elif currVal < 0:
								currVal = 0
							matrices["second_thresholds"].setElem(selector, 0, currVal)
							mutations[3] += 1
							#print("Mutation in second threshold")
			newPopulation.append(matrices)
		self.population = newPopulation
		return mutations

	def roulette(self, scores):
		nextGen = []
		selector = int(random.random() * self.size)
		selectors = []
		beta = 0.0
		mw = max(scores)
		for n in range(self.size):
			pair = []

			## no breeding, just fittest lives
			if False:
				for i in range(2):
					beta += (random.random() * mw * 2.0)
					while (beta > scores[selector]):
						beta -= scores[selector]
						selector = (selector + 1) % self.size

					pair.append(selector)

				## breed the pair
				newCitizens = self.mateParents(pair[0], pair[1])
				nextGen.extend(newCitizens)

			# just random roulette wheel picker and append to next gen..
			else:
				beta += (random.random() * mw * 2.0)
				while (beta > scores[selector]):
					beta -= scores[selector]
					selector = (selector + 1) % self.size
				nextGen.append(copy.deepcopy(self.population[selector]))
				# print("Selected: ", selector)

			selectors.append(selector)

			# if we've grown the next generation to the maxpop size, then finish
			if len(nextGen) >= self.size:
				break

		# print(selectors)
		return nextGen
		# return self.population

	def validate(self):
		"Verifies that the sizes of the internal ANN matrices match those of the settings"
		valid = True
		for p in self.population:
			valid = valid and (p["first_weights"].getWidth() == self.inSize)
			valid = valid and (p["first_weights"].getHeight() == self.hiddenSize)
			valid = valid and (p["first_thresholds"].getWidth() == 1)
			valid = valid and (p["first_thresholds"].getHeight() == self.hiddenSize)
		return valid