import ga

## initialise the GA
oga = ga.ga()
oga.seedGA(2, 10, 8, 4)


pops = oga.getPopulation()
print(pops[0]["first_weights"].renderT())
print(pops[1]["first_weights"].renderT())


print(oga.mutatePopulation(pops, 1, 1))


pops = oga.getPopulation()
print(pops[0]["first_weights"].renderT())
print(pops[1]["first_weights"].renderT())
