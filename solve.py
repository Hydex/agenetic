import re, sys, random
import ga, Matrix, Ann

def tokenise(agent):
	agent = agent.lower()
	p = re.compile(r'[^A-Za-z1-9.]')
	agent = p.sub(' ', agent)
	tokens = agent.split(' ')
	return tokens


def threshold(input, thresholds):
	
	res = Matrix.Matrix()
	
	if (input.getWidth() != 1) or (thresholds.getWidth() != 1):
		throw("input and thresholds must only be 1 column wide")

	res.setWidth(1).setHeight(input.getHeight()).init()
	
	for h in range(input.getHeight()):
		if input.getElem(h, 0) > thresholds.getElem(h, 0):
			res.setElem(h, 0, 1)
	
	return res


def fitnes(results):
	r'do something'
	pass


## Some settings
maxPops = 100			## the maximum number of populations to breed before exiting
popSize = 10			## the number of chromozomes in each population

## Some data structures
strings = {}
userAgents = []

## load the demo data
agents = open("agents.txt", "r")

# setup the output values
outputValues = ["desktop","robot","mobile","tablet"]


# create a list of all tokens found in an agent string
p = re.compile(r'"([^"]+)"')
for agent in agents:
	userAgentStr = p.findall(agent)

	agentDetails = {}
	agentDetails["string"] = userAgentStr[0]
	agentDetails["type"] = userAgentStr[1]
	agentDetails["tokens"] = tokenise(agentDetails["string"])
	userAgents.append(agentDetails)

	# analyse the frequency of each term in strings
	for token in agentDetails["tokens"]:
		if token != '':
			if token not in strings:
				strings[token] = 0
			strings[token] += 1


print("searching across", len(userAgents), "user agent string")


inputValues = list(strings.keys())		## global list of tokens
inputSize = len(inputValues)			## number of tokens == size of the input matrix of the aNN
outputSize = len(outputValues)			## number of states == size of the output matrix of the aNN


## setup the level at which we'll assume the alogorithm has converged
successThreshold = popSize * len(userAgents) * 7.25


print("Sizes:")
print(inputSize, popSize, outputSize)
print("Success Threshold", successThreshold)


## initialise the GA
oga = ga.ga()
oga.seedGA(popSize, inputSize, popSize, outputSize)


## run the analysis no more than maxPops times, if we converge, then we will
## break, however, this prevents it from running too long...
for N in range(maxPops):
	
	# fetch the entire population for this iteration
	pop = oga.getPopulation()

	# scores will hold the fitness for each particular chromozone
	scores = [0 for p in pop]
	sols   = []

	# evaluate each chromozone
	for chromoNum in range(len(pop)):

		chromozome = pop[chromoNum]

		# print("Citizen: ", chromoNum)

		## run an ANN based on the chromozone for each user agent string
		for agent in userAgents:

			correct = outputValues.index(agent["type"])
			
			if correct >= 0:

				# run the ANN with the current chromozome's configuration
				sol = Ann.ann(agent["tokens"], inputValues).solve(chromozome)
				sols.append(sol)

				# score the result and accumulate total fitness over all agents
				fitness = Ann.ann.fitness(None, sol, correct)
				scores[chromoNum] += fitness

			else:
				print("answer", agent["type"], "not found in output variables (", correct, "). Ensure the training data is correct")
				sys.exit()
				## throw("answer #answer# not found in output variables (#correct#). Ensure the training data is correct")


	## Now we score the overall results...
	allMarks = sum(scores)
	# TODO: replace with a list comprehension or reduce function
	sumScores = [0 for s in scores]
	for s in range(len(scores)-1):
		sumScores[s+1] = sumScores[s] + scores[s]


	print("Generation:", N, "TOTAL:", allMarks, len(scores))


	# for each value in scores, select a new value based on the roulette wheel
	nextGen = oga.roulette(scores)


	oga = ga.ga()
	oga.setGA(nextGen)

	if N < maxPops-1:
		oga.getNextPopulation(nextGen, 0.1, 1)

	if allMarks > successThreshold-0.2:
		print("we have convergence!!")
		break



# some rudimentary debug
for x in range(popSize):
	print(sols[x].renderT())
	print(scores[x])
sys.exit()



print(len(sols))
sys.exit()

for s in sols:
	print(s.renderT())
	print()

print("First")
for x in range(inputSize):
	print(pop[0]["first_weights"].getElem(0,x), pop[1]["first_weights"].getElem(0, x))

print("\n", "Second")
for x in range(popSize):
	print(pop[0]["first_thresholds"].getElem(x, 0), pop[1]["first_weights"].getElem(x, 0))

print("\n", "Third")
for x in range(outputSize):
	print(pop[0]["second_weights"].getElem(0,x), pop[1]["second_weights"].getElem(0, x))