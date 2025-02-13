import numpy as np

import opfython.math.general as g
import opfython.stream.splitter as s
import opytimizer.math.random as r
from opfython.models.supervised import SupervisedOPF
from opytimizer import Opytimizer
from opytimizer.core.function import Function
from opytimizer.optimizers.boolean.bpso import BPSO
from opytimizer.spaces.boolean import BooleanSpace
from sklearn.datasets import load_digits

# Loading digits dataset
digits = load_digits()

# Gathering samples and targets
X = digits.data
Y = digits.target

# Adding 1 to labels, i.e., OPF should have labels from 1+
Y += 1

# Splitting data into training and testing sets
X_train, X_val, Y_train, Y_val = s.split(
    X, Y, percentage=0.5, random_state=1)


def supervised_opf_feature_selection(opytimizer):
    # Gathering features
    features = opytimizer[:, 0].astype(bool)

    # Remaking training and validation subgraphs with selected features
    X_train_selected = X_train[:, features]
    X_val_selected = X_val[:, features]

    # Creates a SupervisedOPF instance
    opf = SupervisedOPF(distance='log_squared_euclidean',
                        pre_computed_distance=None)

    # Fits training data into the classifier
    opf.fit(X_train_selected, Y_train)

    # Predicts new data
    preds = opf.predict(X_val_selected)

    # Calculating accuracy
    acc = g.opf_accuracy(Y_val, preds)

    return 1 - acc


# Creating Function's object
f = Function(pointer=supervised_opf_feature_selection)

# Number of agents
n_agents = 5

# Number of decision variables
n_variables = 64

# Number of running iterations
n_iterations = 3

# Creating the SearchSpace class
b = BooleanSpace(n_agents=n_agents, n_iterations=n_iterations,
                 n_variables=n_variables)

# Hyperparameters for the optimizer
hyperparams = {
    'c1': r.generate_binary_random_number(size=(n_variables, 1)),
    'c2': r.generate_binary_random_number(size=(n_variables, 1))
}

# Creating BPSO's optimizer
p = BPSO(hyperparams=hyperparams)

# Finally, we can create an Opytimizer class
o = Opytimizer(space=b, optimizer=p, function=f)

# Running the optimization task
history = o.start()
