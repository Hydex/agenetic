import ga

## initialise the GA
oga = ga.ga()
oga.seedGA(2, 10, 8, 4)


pops = oga.getPopulation()
print(pops[0]["first_weights"].renderT())
print(pops[1]["first_weights"].renderT())


newGen = oga.roulette([10, 10], True)
oga.setGA(newGen)


pops = oga.getPopulation()
print(pops[0]["first_weights"].renderT())
print(pops[1]["first_weights"].renderT())
