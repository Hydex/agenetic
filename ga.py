import Matrix, random

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

	def setGA(self, population):
		self.population = population
		temp = population[0]
		self.inSize = temp["first_weights"].getHeight()
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

	def getNextPopulation(self, survivors, mutationRate, crossOver):
		newPopulation = []
		for matrices in survivors:
			# matrices = self.population[s]
			if random.random() < mutationRate:
				selector = int(random.random() * self.coeff_size)
				#print("selector:", selector, self.coeff_size)
				if selector < (self.inSize * self.hiddenSize):
					selector_row = int(selector/self.inSize)
					selector_col = selector % self.inSize
					matrices["first_weights"].setElem(selector_row, selector_col, random.random())
					print("Mutation in first matrix", selector, selector_row, selector_col)
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
						print("Mutation in first threshold", selector)
						pass
					else:
						selector = selector - (self.hiddenSize)
						if selector < (self.hiddenSize * self.outSize):
							selector_row = int(selector/self.inSize)
							selector_col = selector % self.hiddenSize
							matrices["second_weights"].setElem(selector_row, selector_col, random.random())
							print("Mutation in second matrix", selector, selector_row, selector_col)
						else:
							selector = selector - (self.hiddenSize * self.outSize)
							currVal = matrices["second_thresholds"].getElem(selector, 0)
							currVal += (0.1 - random.random()*0.2)
							if currVal > 2:
								currVal = 2
							elif currVal < 0:
								currVal = 0
							matrices["second_thresholds"].setElem(selector, 0, currVal)
							#print("Mutation in second threshold")
			newPopulation.append(matrices)
		self.population = newPopulation

	def roulette(self, scores):
		nextGen = []
		selector = int(random.random() * self.size)
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
				nextGen.append(pop[selector])

			# if we've grown the next generation to the maxpop size, then finish
			if len(nextGen) >= self.size:
				break

		return nextGen
