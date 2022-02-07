# Using analyzers

import covasim as cv
cv.options(jupyter=True, verbose=0)

# The below analyzer creates a age-specific distribution of metrics (rather than examining the entire population)
sim = cv.Sim(interventions=cv.test_prob(0.5), analyzers=cv.age_histogram())
sim.run()
agehist = sim.get_analyzer() # Only one analyzer so we can retrieve it like this
agehist.plot()

# Transmission trees
tt = sim.make_transtree()
fig1 = tt.plot()
fig2 = tt.plot_histograms()

# Custom analyzers
# Used to analyze the daily state of People and plot the results as the simulation progresses
# Might be useful when plotting symptom distributions for people over the course of the simulation
import pylab as pl
import sciris as sc

class store_seir(cv.Analyzer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # This is necessary to initialize the class properly
        self.t = []
        self.S = []
        self.E = []
        self.I = []
        self.R = []
        return

    def apply(self, sim):
        ppl = sim.people # Shorthand
        self.t.append(sim.t)
        self.S.append(ppl.susceptible.sum())
        self.E.append(ppl.exposed.sum() - ppl.infectious.sum())
        self.I.append(ppl.infectious.sum())
        self.R.append(ppl.recovered.sum() + ppl.dead.sum())
        return

    def plot(self):
        pl.figure()
        pl.plot(self.t, self.S, label='S')
        pl.plot(self.t, self.E, label='E')
        pl.plot(self.t, self.I, label='I')
        pl.plot(self.t, self.R, label='R')
        pl.legend()
        pl.xlabel('Day')
        pl.ylabel('People')
        sc.setylim() # Reset y-axis to start at 0
        sc.commaticks() # Use commas in the y-axis labels
        return

sim = cv.Sim(n_days=180, analyzers=store_seir(label='seir'))
sim.run()
seir = sim.get_analyzer('seir') # Retrieve by label
seir.plot()

# Another analyzer but it does not require the state of the People
def check_88(sim):
    people_who_are_88 = sim.people.age.round() == 88 # Find everyone who's aged 88 (to the nearest year)
    people_exposed = sim.people.exposed # Find everyone who's infected with COVID
    # Logical and to find the set of all people who are 88 and exposed
    people_who_are_88_with_covid = cv.true(people_who_are_88 * people_exposed) # Multiplication is the same as logical "and"
    n = len(people_who_are_88_with_covid) # Count how many people there are
    if n:
        print(f'Oh no! {n} people aged 88 have covid on timestep {sim.t} {"🤯"*n}')
    return

sim = cv.Sim(n_days=120, analyzers=check_88, verbose=0)
sim.run()