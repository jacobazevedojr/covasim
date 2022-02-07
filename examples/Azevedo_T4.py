import covasim as cv
# Data requirements
# Population Size
# Deaths per day
# Diagnosed cases per day

# Optional, but desired data
# Seroprevalence
# Tests per day
# Vaccinations per day
# Policy interventions

# Demographic Data
# Note data format and key names!
# Below is a dictionary of the population distribution of Johannesburg
joburg_pop = {
   '0-9':  286620,
  '10-19': 277020,
  '20-29': 212889,
  '30-39': 161329,
  '40-49': 104399,
  '50-59': 51716,
  '60-69': 36524,
  '70-79': 22581,
  '80+':   7086,
}

cv.data.country_age_data.data['Johannesburg'] = joburg_pop

# Epidemiological data scrapers
import pandas as pd
df = pd.read_csv('docs/tutorials/example_data.csv')
print(df)
# ^ This is the correct data format for covasim
'''
          date  new_diagnoses  new_tests  new_deaths
0   2020-03-01              1         24           0
1   2020-03-02              3         22           0
2   2020-03-03              2         15           0
3   2020-03-04              8         40           0
4   2020-03-05             20         38           0
5   2020-03-06              9         61           0
6   2020-03-07              6         43           0
7   2020-03-08             13         98           0
8   2020-03-09              6         93           0
9   2020-03-10             25        170           0
10  2020-03-11             28        368           0
11  2020-03-12             27        437           0
12  2020-03-13             22        291           2
13  2020-03-14             43        328           0
14  2020-03-15             76       1147           0
15  2020-03-16             65       1438           1
16  2020-03-17             88       1209           0
17  2020-03-18             86       1269           0
18  2020-03-19            115       1195           1
19  2020-03-20             51        529           0
20  2020-03-21             55        482           3
21  2020-03-22             95       1106           2
22  2020-03-23             74        471           1
23  2020-03-24             63        438           4
24  2020-03-25            178       1111           2
25  2020-03-26             83        621           1
26  2020-03-27            140       1059           2
27  2020-03-28            137        951           1
28  2020-03-29            150        964           0
29  2020-03-30            144       1058           1
30  2020-04-03            145       1058           1
31  2020-04-11              0          0           1
'''
# Column w/ date
# Column with new_ or cum_ to start and a combination of: tests, diagnoses, deaths, severe (hospitalizations), or critical (ICU)

# Example of importing data and using it for simulation
cv.options(verbose=0)

pars = dict(
    start_day = '2020-02-01',
    end_day   = '2020-04-11',
    beta      = 0.015,
)
sim = cv.Sim(pars=pars, datafile='example_data.csv', interventions=cv.test_num(daily_tests='data'))
sim.run()
sim.plot(['cum_tests', 'cum_diagnoses', 'cum_deaths'])

# This doesn't fit to the data well, so the model must be calibrated first

# Example of loading population data
pars = dict(
    pop_size = 10_000, # Alternate way of writing 10000
    pop_type = 'hybrid',
    location = 'Bangladesh', # Case insensitive
)

sim = cv.Sim(pars)
sim.initialize() # Create people
fig = sim.people.plot() # Show statistics of the people

# Saving the initialized population
import sciris as sc # We'll use this to time how long each one takes

pars = dict(n_agents=50e3, pop_type='hybrid')

with sc.timer('creating'):
    sim1 = cv.Sim(pars).init_people()

# Will save the population to use for later
sim1.people.save('my-people.ppl')

with sc.timer('loading'):
    sim2 = cv.Sim(pars, popfile='my-people.ppl').init_people()