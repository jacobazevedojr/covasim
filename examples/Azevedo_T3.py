# Running Multisims

import covasim as cv
cv.options(jupyter=True, verbose=0)

sim = cv.Sim()
msim = cv.MultiSim(sim)
msim.run(n_runs=5)
msim.plot()

# Each single sim is stored in the msim.sims attribute
for sim in msim.sims:
    sim.brief()

# Plotting the mean
msim.mean()
msim.plot_result('new_infections')

# Plotting the median
msim.median()
msim.plot_result('new_infections')

# If you want each sim to just be a parallel version of itself, you can combine them all
msim.combine()
msim.plot_result('new_infections')

# Running different sims (not just the same sim w/ different seeds)
import numpy as np

betas = np.linspace(0.010, 0.020, 5) # Sweep beta from 0.01 to 0.02 with 5 values
sims = []
for beta in betas:
    sim = cv.Sim(beta=beta, label=f'Beta = {beta}')
    sims.append(sim)
msim = cv.MultiSim(sims)
msim.run()
msim.plot_result('cum_infections')

# Scenarios
# Set base parameters -- these will be shared across all scenarios
basepars = {'pop_size':10e3}

# Configure the settings for each scenario
scenarios = {'baseline': {
              'name':'Baseline',
              'pars': {}
              },
            'high_beta': {
              'name':'High beta (0.020)',
              'pars': {
                  'beta': 0.020,
                  }
              },
            'low_beta': {
              'name':'Low beta (0.012)',
              'pars': {
                  'beta': 0.012,
                  }
              },
             }

# Run and plot the scenarios
scens = cv.Scenarios(basepars=basepars, scenarios=scenarios)
scens.run()
scens.plot()