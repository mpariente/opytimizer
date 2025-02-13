from opytimizer.optimizers.boolean.bpso import BPSO

# One should declare a hyperparameters object based
# on the desired algorithm that will be used
hyperparams = {
    'w': 1,
    'c1': 0,
    'c2': 1
}

# Creating a BPSO optimizer
o = BPSO(hyperparams=hyperparams)
