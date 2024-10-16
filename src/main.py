import os
import datetime
import numpy as np

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.visualization.scatter import Scatter

from instance import read_instance
from bi_objective_generalized_diversity_problem import BiObjectiveGeneralizedDiversityProblem


path = os.path.join('USCAP.txt')
instance = read_instance(path)


dist_matrix = np.array(instance['d'])  # Distance matrix

costs = np.array(instance['a'])  # Costs for each node
capacities = np.array(instance['c'])  # Capacities for each node
B = instance['B']  # Minimum required capacity
K = instance['K']  # Maximum allowed budget

n = instance['n']

start = datetime.datetime.now()

# Create the problem instance
problem = BiObjectiveGeneralizedDiversityProblem(dist_matrix, costs, capacities, B, K)

# Configure the NSGA-II algorithm
algorithm = NSGA2(
    pop_size=100,
    sampling=BinaryRandomSampling(),
    crossover=TwoPointCrossover(),
    mutation=BitflipMutation(),
    eliminate_duplicates=True
)

# Set termination criteria
termination = get_termination("n_gen", 200)

# Run the optimization
res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               save_history=True,
               verbose=True)

elapsed = datetime.datetime.now() - start

# Visualize the Pareto front (objective space)
plot = Scatter()
plot.add(-res.F, color="red")
plot.show()

# Print the best solutions found
print("Best solutions (with binary decision variables):")
for sol in res.X:
    print(sol)
