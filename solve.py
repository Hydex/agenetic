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



import re, sys, random
import ga, Matrix, Ann

def tokenise(agent):
	agent = agent.lower()
	tokens = []

	p = re.compile(r'[A-Za-z1-9](?:\.[A-Za-z1-9]+|[A-Za-z1-9]+)')
	tokens = p.findall(agent)

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
maxPops = 500			## the maximum number of populations to breed before exiting
popSize = 10			## the number of chromozomes in each population
muationProb = 0.1 		## the chance that a population mutates.

debugEvery = 1 			## the number of iterations where debug info is written to screen

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


inputValues = list(strings.keys())		## global list of tokens
inputSize = len(inputValues)			## number of tokens == size of the input matrix of the aNN
outputSize = len(outputValues)			## number of states == size of the output matrix of the aNN


## setup the level at which we'll assume the alogorithm has converged
# successThreshold = popSize * len(userAgents) * 7.25
# successThreshold = len(userAgents) * 24
userAgentsLen = len(userAgents)
successThreshold = userAgentsLen * 40


print("searching across", len(userAgents), "user agent string")
print("Sizes:")
print("Input Strings:", inputSize)
print("Population size:", popSize)
print("Output size:", outputSize)
print("Success Threshold", successThreshold, "\n")


## initialise the GA
oga = ga.ga()
oga.seedGA(popSize, inputSize, 100, outputSize)

if not oga.validate():
	print("GA doesn't validate")
	sys.exit()

t = oga.getPopulation()[0]["first_weights"]
print("First Weights:", t.getWidth(), "x", t.getHeight(), len(t.getData()[0]), len(t.getData()), oga.getInputSize(), oga.getHiddenSize())
# print("First Weights:", oga.getPopulation()[0]["first_weights"].getWidth(), "x", oga.getPopulation()[0]["first_weights"].getHeight())
# print("Seconds Weights:", oga.getPopulation()[0]["second_weights"].getWidth(), "x", oga.getPopulation()[0]["second_weights"].getHeight())
# print("Seconds Weights:", oga.getPopulation()[0]["second_weights"].getWidth(), "x", oga.getPopulation()[0]["second_weights"].getHeight())

## run the analysis no more than maxPops times, if we converge, then we will
## break, however, this prevents it from running too long...
for N in range(maxPops):
	
	# fetch the entire population for this iteration
	pop = oga.getPopulation()

	# scores will hold the fitness for each particular chromozone
	scores 	= [0 for p in pop]
	sols	= []
	best	= 0
	worst	= 0

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

		# after testing every input example, if we have reached the threshold, we're done!
		if scores[chromoNum] >= successThreshold-0.2:
			print("we have convergence!!")
			break


	## Now we score the overall results...
	# allMarks = sum(scores)
	# TODO: replace with a list comprehension or reduce function
	# sumScores = [0 for s in scores]
	# for s in range(len(scores)-1):
	# 	sumScores[s+1] = sumScores[s] + scores[s]


	# for each value in scores, select a new value based on the roulette wheel
	nextGen = oga.roulette(scores)
	oga = ga.ga()
	oga.setGA(nextGen)

	if N < maxPops-1:
		mutations = oga.mutatePopulation(nextGen, muationProb, 1)
	else:
		mutations = []


	## show some useful output
	if N % debugEvery == 0:
		print("Generation:", N, "TOTAL:", sum(scores), mutations, "best:", max(scores), "worst:", min(scores))
		print("Scores:", scores, "\n")



	# some rudimentary debug
	if N % 25 == 0:
		for x in range(popSize):
			for i in range(outputSize):
				for agent in range(userAgentsLen):
					solutionNum = (x * userAgentsLen) + agent
					m = sols[solutionNum]
					print("|", sep="", end=" ")
					print(m.getElem(i, 0), sep="", end=" ")
					print("|", end="")
				print("")
				# print(sols[x].renderT())
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