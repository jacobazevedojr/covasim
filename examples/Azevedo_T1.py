import covasim as cv

'''Step 1'''
'''
sim = cv.Sim()
sim.run()
fig = sim.plot()
'''

'''Step 2'''
pars = dict(
    pop_size=50e3,
    pop_infected=100,
    start_day='2020-04-01',
    end_day='2020-06-01',
)

sim = cv.Sim(pars)
sim.run()
# Generates results dictionary in sim.results
# sim.results['new_infections']