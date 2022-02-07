# Calibration

import covasim as cv
cv.options(verbose=0)

pars = dict(
    pop_size  = 20_000,
    start_day = '2020-02-01',
    end_day   = '2020-04-11',
    beta      = 0.015,
)
sim = cv.Sim(pars=pars, datafile='example_data.csv', interventions=cv.test_num(daily_tests='data'))
sim.run()
sim.plot(to_plot=['cum_tests', 'cum_diagnoses', 'cum_deaths'])

# Notice this model does not fit the data well
fit = sim.compute_fit()
print(fit.mismatches)
print(fit.mismatch)


# Notice the cum_deaths fit is too low so we increase the death probability to better fit the data
sim['rel_death_prob'] = 2 # Double the death rate since deaths were too low
sim.initialize(reset=True) # Reinitialize the sim

# Rerun and compute fit
sim.run()
fit = sim.compute_fit()

# Output
sim.plot()
fit.plot()
print(fit.mismatches)
print(fit.mismatch)

# Using scipy to optimize the parameters used in the covasim simulation
import numpy as np
import scipy

def objective(x, n_runs=10):
    print(f'Running sim for beta={x[0]}, rel_death_prob={x[1]}')
    pars = dict(
        pop_size       = 20_000,
        start_day      = '2020-02-01',
        end_day        = '2020-04-11',
        beta           = x[0],
        rel_death_prob = x[1],
        verbose        = 0,
    )
    sim = cv.Sim(pars=pars, datafile='/home/cliffk/idm/covasim/docs/tutorials/example_data.csv', interventions=cv.test_num(daily_tests='data'))
    msim = cv.MultiSim(sim)
    msim.run(n_runs=n_runs)
    mismatches = []
    for sim in msim.sims:
        fit = sim.compute_fit()
        mismatches.append(fit.mismatch)
    mismatch = np.mean(mismatches)
    return mismatch

guess = [0.015, 1] # Initial guess of parameters -- beta and relative death probability
pars = scipy.optimize.minimize(objective, x0=guess, method='nelder-mead') # Run the optimization

# A more automated approach
# must install optuna -> pip install optuna
# Unlocks the method sim.calibrate()
# Still requires manually tuning parameters until fit is improved.

'''
Example for running built-in calibration with Optuna
'''

import sciris as sc

# Create default simulation
pars = sc.objdict(
    pop_size       = 20_000,
    start_day      = '2020-02-01',
    end_day        = '2020-04-11',
    beta           = 0.015,
    rel_death_prob = 1.0,
    interventions  = cv.test_num(daily_tests='data'),
    verbose        = 0,
)
sim = cv.Sim(pars=pars, datafile='example_data.csv')

# Parameters to calibrate -- format is best, low, high
calib_pars = dict(
    beta           = [pars.beta, 0.005, 0.20],
    rel_death_prob = [pars.rel_death_prob, 0.5, 3.0],
)

if __name__ == '__main__':

    # Run the calibration
    n_trials = 20
    n_workers = 4
    calib = sim.calibrate(calib_pars=calib_pars, n_trials=n_trials, n_workers=n_workers)