'''
This file is a driver to show how symptom simulation is performed on top of covasim's base simulation
'''

import covasim as cv

pars = dict(
    pop_size = 50e3, # Have 50,000 people total in the population
    pop_infected = 100, # Start with 100 infected people
    n_days = 365, # Run the simulation for 90 days
    verbose = 1, # Do not print any output
)

if __name__ == '__main__':
    sim = cv.Sim(pars, label='Symptom Simulation')
    sim.run()
    fig = sim.plot(to_plot=['cum_deaths', 'cum_infections'])