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

	def mateParents(self, firstParentId, secondParentId, intest=False):
		'''Takes the ids of two chromozones, picks a crossover point and then
		takes the first part of chromozone one, before the crossover location
		and joins it with the second part of chromozone two, after the crossover
		location. It then does the opposite with the first part of chromozone two
		and the second part of chromozone one.'''
		parent1 = self.population[firstParentId]
		parent2 = self.population[secondParentId]
		selector = int(random.random() * self.coeff_size)
		children = [parent1.copy(), parent2.copy()]
		crossover_index = 0

		if intest:
			print("Mating parents:", selector)

		# print("selector:", selector, self.coeff_size)
		if selector < (self.inSize * self.hiddenSize):
			selector_row = int(selector/self.inSize)
			selector_col = selector % self.inSize
			crossover_loc = "first_weights"
			crossover_index = 0
			# print("Crossing first weights", selector, selector_row, selector_col)
		else:
			# child["first_weights"] = parent1["first_weights"].copy()
			selector = selector - (self.inSize * self.hiddenSize)
			if selector < self.hiddenSize:
				selector_row = selector
				selector_col = 0
				crossover_loc = "first_thresholds"
				crossover_index = 1
				# print("Crossing first thresholds", selector, selector_row, selector_col)
			else:
				# child["first_thresholds"] = parent1["first_thresholds"].copy()
				selector = selector - (self.hiddenSize)
				if selector < (self.hiddenSize * self.outSize):
					selector_row = int(selector/self.hiddenSize)
					selector_col = selector % self.hiddenSize
					crossover_loc = "second_weights"
					crossover_index = 2
					# print("Crossing second weights", selector, selector_row, selector_col)
				else:
					# child["second_weights"] = parent1["second_weights"].copy()
					selector = selector - (self.hiddenSize * self.outSize)
					selector_row = selector
					selector_col = 0
					crossover_loc = "second_thresholds"
					crossover_index = 3
					# print("Crossing second thresholds", selector, selector_row, selector_col)

		if intest:
			print("Crossover location:", crossover_loc)

		children[0][crossover_loc] = self.crossOver(parent1[crossover_loc], parent2[crossover_loc], selector_row, selector_col)
		children[1][crossover_loc] = self.crossOver(parent2[crossover_loc], parent1[crossover_loc], selector_row, selector_col)

		## then merge the remaining matrices into the new chromozone
		if crossover_index < 1:
			children[0]['first_thresholds'] = copy.deepcopy(parent2['first_thresholds'])
			children[1]['first_thresholds'] = copy.deepcopy(parent1['first_thresholds'])
		if crossover_index < 2:
			children[0]['second_weights'] = copy.deepcopy(parent2['second_weights'])
			children[1]['second_weights'] = copy.deepcopy(parent1['second_weights'])
		if crossover_index < 3:
			children[0]['second_thresholds'] = copy.deepcopy(parent2['second_thresholds'])
			children[1]['second_thresholds'] = copy.deepcopy(parent1['second_thresholds'])

		return children

	def crossOver(self, parent_one, parent_two, row, col, intest=False):
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
		'''Mutates a population of chromozones.

		There are number of approaches to achieving this. This approach uses a primary
		random number in the range (0..3) to select which of the 4 matrices in the ANN
		to mutate. Once it has picked which one, it uses a second random number in the
		range (0..number_of_elements) to choose which value to change.

		This is simplistic, in comparison with another algorithm, which biases the
		probability by the size of the matrix. This approach causes mutations on the
		smaller matrices much more frequently.'''
		newPopulation = []
		mutations = [0 for i in range(4)]
		for matrices in survivors:
			# matrices = self.population[s]
			if random.random() < mutationRate:
				matrixToMutate = int(random.random() * 4)
				print("Mutating", str(matrixToMutate))

				# selector refers to the first weights matrix ([ INPUT x HIDDEN ])
				if matrixToMutate == 0:
					selector_col = int(random.random() * self.inSize)
					selector_row = int(random.random() * self.hiddenSize)
					matrices["first_weights"].setElem(selector_row, selector_col, random.random())
					mutations[0] += 1

				# selector refers to the first thresholds matrix
				elif matrixToMutate == 1:
					selector = int(random.random() * self.hiddenSize)
					currVal = matrices["first_thresholds"].getElem(selector, 0)
					currVal += (0.1 - random.random()*0.2)
					if currVal > 2:
						currVal = 2
					elif currVal < 0:
						currVal = 0
					matrices["first_thresholds"].setElem(selector, 0, currVal)
					mutations[1] += 1
					# print("Mutation in first threshold", selector)

				# selector refers to the second weights matrix ([ HIDDEN x OUTPUT ])
				elif matrixToMutate == 2:
					selector_col = int(random.random() * self.hiddenSize)
					selector_row = int(random.random() * self.outSize)
					matrices["second_weights"].setElem(selector_row, selector_col, random.random())
					mutations[2] += 1
					# print("Mutation in second matrix", selector, selector_row, selector_col)

				# selector refers to the second thresholds
				elif matrixToMutate == 3:
					selector = int(random.random() * self.outSize)
					currVal = matrices["second_thresholds"].getElem(selector, 0)
					currVal += (0.1 - random.random()*0.2)
					if currVal > 2:
						currVal = 2
					elif currVal < 0:
						currVal = 0
					matrices["second_thresholds"].setElem(selector, 0, currVal)
					mutations[3] += 1
					#print("Mutation in second threshold")

				else:
					print("Unknown index for the matrix to mutate:", matrixToMutate)

			newPopulation.append(matrices)
		self.population = newPopulation
		return mutations

	def mutatePopulationSingle(self, survivors, mutationRate, crossOver):
		newPopulation = []
		mutations = [0 for i in range(4)]
		for matrices in survivors:
			# matrices = self.population[s]
			if random.random() < mutationRate:
				selector = int(random.random() * self.coeff_size)
				# selector refers to the first weights matrix
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
					# selector refers to the first thresholds matrix
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
						# selector refers to the second weights matrix
						if selector < (self.hiddenSize * self.outSize):
							selector_row = int(selector/self.outSize)
							selector_col = selector % self.outSize
							matrices["second_weights"].setElem(selector_row, selector_col, random.random())
							mutations[2] += 1
							# print("Mutation in second matrix", selector, selector_row, selector_col)
						# selector refers to the second thresholds
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

	def roulette(self, scores, intest=False):
		nextGen = []
		selector = int(random.random() * self.size)
		selectors = []
		beta = 0.0
		mw = max(scores)
		roul = roulette(scores)

		for n in range(self.size):
			pair = []

			## no breeding, just fittest lives
			if intest:
				pair = [0, 1]
				print("Testing crossover,", pair)

				## breed the pair
				nextGen.extend(self.mateParents(pair[0], pair[1], intest))

			# purely for testing
			if True:
				for i in range(2):
					pair.append(roul.getNext())

				## breed the pair
				nextGen.extend(self.mateParents(pair[0], pair[1]))

			# just random roulette wheel picker and append to next gen..
			else:
				nextGen.append(copy.deepcopy(self.population[roul.getNext()]))
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



class roulette:

	def __init__(self, counts):
		self.data = counts
		self.mw = sum(self.data)
		self.size = len(self.data)
		self.beta = 0
		self.selector = 0

	def getNext(self):
		self.beta += (random.random() * self.mw * 2.0)
		while (self.beta > self.data[self.selector]):
			self.beta -= self.data[self.selector]
			self.selector = (self.selector + 1) % self.size
		return self.selector
