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



import ga, Matrix, Ann, copy, random

## initialise the GA
oga = ga.ga()
oga.seedGA(5, 20, 5, 4)

for p in oga.getPopulation():
	print(p["second_thresholds"])
	print(p["second_thresholds"].renderT())

pop = oga.getPopulation()

newPop = []

for n in range(5):
	newPop.append(copy.deepcopy(pop[0]))
	currVal = newPop[n]["second_thresholds"].getElem(1, 0)
	currVal += (0.1 - random.random()*0.2)
	newPop[n]["second_thresholds"].setElem(1, 0, currVal)

print("New Pop")
for p in newPop:
	print(p["second_thresholds"])
	print(p["second_thresholds"].renderT())


## now test the roulette process
roulettePop = oga.roulette([1,1,1,1,1])

print("Roulette Pop")
for p in roulettePop:
	print(p["second_thresholds"])
	print(p["second_thresholds"].renderT())


## Finally, test the mutation...
mga = ga.ga()
mga.setGA(roulettePop)
mga.mutatePopulation(roulettePop, 0.1, 1)

print("Mutated Pop")
for p in mga.getPopulation():
	print(p["second_thresholds"])
	print(p["second_thresholds"].renderT())
