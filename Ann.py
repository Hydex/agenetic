import Matrix

class ann:

	def __init__(self, tokens, fullSet):
		self.inputVector = Matrix.Matrix()
		self.inputVector.setWidth(1).setHeight(len(fullSet)).init()
		for t in tokens:
			if t in fullSet:
				self.inputVector.setElem(fullSet.index(t), 0, 1)
		self.inputSize = len(fullSet)
		# print("validStrings", self.inputVector.getWidth(), self.inputVector.getHeight())

	def solve(self, ann):
		M = Matrix.Matrix()
		## run the weights --->
		acc1 = M.multiply(self.inputVector, ann["first_weights"])
		acc1 = acc1.divide(self.inputSize)
		acc2 = self.threshold(acc1, ann["first_thresholds"])
		acc3 = M.multiply(acc2, ann["second_weights"])
		acc4 = self.threshold(acc3, ann["second_thresholds"])

		return acc4

	def fitness(self, solution, correct):
		score = 0
		badvals = 0
		# evaluate the 'fitness' for the output.
		# we'll use:
		#	1	for a right bit
		#	0	for a wrong bit
		for ic in range(solution.getHeight()):
			if solution.getElem(ic, 0) == 1 and ic == correct:
				score += 1.5
			elif solution.getElem(ic, 0) == 0 and ic != correct:
				score += 0.25
			else:
				badvals += 1
		if badvals == 0:
			score += 5
		else:
			score -= badvals * 0.25
		if score < 0.25:
			score = 0.25
		return score

	# apply the threshold level to the incoming values
	def threshold(self, values, levels):
		if (values.getHeight() != levels.getHeight()):
			print("the heights of both matrices must be equal")
			sys.exit()
		M = Matrix.Matrix().setWidth(1).setHeight(values.getHeight()).init()
		for h in range(values.getHeight()):
			if (values.getElem(h, 0) > levels.getElem(h, 0)):
				M.setElem(h, 0, 1)
		return M