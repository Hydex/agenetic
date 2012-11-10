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


## Some settings
maxPops = 100			## the maximum number of populations to breed before exiting
popSize = 10			## the number of chromozomes in each population



strings = {}
userAgents = []

## <cffile action="read" file="#GetDirectoryFromPath(GetCurrentTemplatePath())#/agents.txt" variable="agents">
agents = open("agents.txt", "r")

# setup the output values
outputValues = ["desktop","robot","mobile","tablet"]

# create a list of all tokens found in an agent string
p = re.compile(r'"([^"]+)"')
for agent in agents:
	userAgentStr = p.findall(agent)

	# <cfset correct = ArrayFind(outputValues, answer)>
	
	agentDetails = {}
	agentDetails["string"] = userAgentStr[0]
	agentDetails["type"] = userAgentStr[1]
	userAgents.append(agentDetails)

	# break up the agent string and record the frequency of each term
	tokens = tokenise(agentDetails["string"])
	for token in tokens:
		# print("token", token)
		if token != '':
			if token not in strings:
				strings[token] = 0
			strings[token] += 1


# toremove = []
# for x in strings:
# 	if strings[x] == 1:
# 		toremove.append(x)
# for x in toremove:
# 	del strings[x]

print("searching across", len(userAgents), "user agent string")
inputValues = list(strings.keys())


inputSize = len(inputValues)
hiddenSize = popSize
outputSize = len(outputValues)

successThreshold = popSize * len(userAgents) * 7.25


print("Sizes:")
print(inputSize, hiddenSize, outputSize)

print("Success Threshold", successThreshold)


oga = ga.ga()
oga.seedGA(popSize, inputSize, hiddenSize, outputSize)


## run the analysis N times
for N in range(maxPops):
	
	pop = oga.getPopulation()


	## figure out the fitness for each populate --->
	scores = [0 for p in pop]
	sols   = []

	for annCount in range(len(pop)):

		chromozome = pop[annCount]

		# print("Citizen: ", annCount)

		## run each ANN and get the result
		for agent in userAgents:

			correct = outputValues.index(agent["type"])
			
			if correct >= 0:

				# break up the agent string into valid tokens
				tokens = tokenise(agent["string"])
				
				# run the ANN with the current chromozome's configuration
				ann = Ann.ann(tokens, inputValues)
				sol = ann.solve(chromozome)
				sols.append(sol)

				# score the result and accumulate total fitness over all agents
				fitness = ann.fitness(sol, correct)
				scores[annCount] += fitness

			else:
				print("answer", agent["type"], "not found in output variables (", correct, "). Ensure the training data is correct")
				sys.exit()
				## throw("answer #answer# not found in output variables (#correct#). Ensure the training data is correct")

			# print(agent["string"], correct, sol.renderT(), fitness, sep="\n")


	allMarks = sum(scores)
	# TODO: replace with a list comprehension or reduce function
	sumScores = [0 for s in scores]
	sumScores[0] = 0
	for s in range(len(scores)-1):
		sumScores[s+1] = sumScores[s] + scores[s]

	print("Generation:", N, "TOTAL:", allMarks, len(scores))

	# for each value in scores, select a new value based on the roulette wheel
	nextGen = []
	selector = int(random.random() * popSize)
	beta = 0.0
	mw = max(scores)
	for n in range(popSize):
		pair = []

		## no breeding, just fittest lives
		if False:
			for i in range(2):
				beta += (random.random() * mw * 2.0)
				while (beta > scores[selector]):
					beta -= scores[selector]
					selector = (selector + 1) % popSize

				pair.append(selector)

			## breed the pair
			#print(n, "Breed pair", pair)
			newCitizens = oga.mateParents(pair[0], pair[1])
			nextGen.extend(newCitizens)

		# just random roulette wheel picker and append to next gen..
		else:
			beta += (random.random() * mw * 2.0)
			while (beta > scores[selector]):
				beta -= scores[selector]
				selector = (selector + 1) % popSize
			nextGen.append(pop[selector])

		# if we've grown the next generation to the maxpop size, then finish
		if len(nextGen) >= popSize:
			break

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
for x in range(hiddenSize):
	print(pop[0]["first_thresholds"].getElem(x, 0), pop[1]["first_weights"].getElem(x, 0))

print("\n", "Third")
for x in range(outputSize):
	print(pop[0]["second_weights"].getElem(0,x), pop[1]["second_weights"].getElem(0, x))