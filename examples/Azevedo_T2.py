import covasim as cv

cv.options(verbose=0) # Standard options for Jupyter notebook

sim = cv.Sim()
sim.run()

sim.brief()

print()

sim.summarize()

print()

sim.disp()

# Plotting
import pylab as pl # Shortcut for import matplotlib.pyplot as plt
# Plots x and y sets (but is not formatted nicely)
pl.plot(sim.results['date'], sim.results['new_infections'])

# As an alternative
sim.plot(to_plot=['new_infections', 'cum_infections'])
# To plot everything
sim.plot('overview', n_cols=5, figsize=(20,20), dateformat='concise', dpi=50) # NB: dateformat='concise' is already the default for >2 columns


# Saving figures
cv.savefig('my-fig.png')
# Printing figure metadata
cv.get_png_metadata('my-fig.png')

# Plot styles
sim.plot(style='seaborn-whitegrid') # built in matplotlib style

# Saving simulations
sim.save('my-awesome-sim.sim')
# Loading simulations
sim = cv.load('my-awesome-sim.sim')

# Exporting to excel
sim.to_excel('my-sim.xlsx')
df = pd.read_excel('my-sim.xlsx')
print(df)
