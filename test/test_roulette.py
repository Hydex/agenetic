## create a highly asymetric set of fitnesses and asses how well roulette picks the next population

import ga, copy

scores = [[1,1,1,1,1,1,1,1,1,100],
		  [1,50,50,1,1,1,1,1,1,100],
		  [20,0,20,0,20,0,20,0,20,0]]
reps = 10000
pop = [0,1,2,3,4,5,6,7,8,9]

for s in scores:

	print("Testing:", s)
	oga = ga.ga()
	oga.setGA2(pop)

	counts = [0 for x in s]

	for n in range(reps):
		newPop = oga.roulette(s)
		for p in newPop:
			counts[p] += 1

	sumScores = sum(s)
	expScores = copy.copy(s)
	for i in range(len(s)):
		expScores[i] = (s[i] / sumScores) * reps * len(s)
		print(counts[i], expScores[i])

	print("\n")