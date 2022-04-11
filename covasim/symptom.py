"""
This file defines all additional methods for implementing a symptom simulation model
"""

# Implemented based on "Modeling the Onset of Symptoms of COVID-19"
# Larsen J., Martin M., Martin J., Kuhn P., Hicks J.

# Utilizes a Markov Process to a "graded partially ordered set based on clinical observations of COVID-19
# cases to ascertain the most likely order of discernible symptoms (i.e. fever, cough, nausea/vomiting, and
# diarrhea)"

# Then compares symptom progression of COVID-19 to other respiratory diseases: influenza, SARS, and MERS

# Markov Process: stochastic sequence of events in which the likelihood of the next state only depends on
# the current state rather than past or future states

