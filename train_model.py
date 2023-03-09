from sklearn.neighbors import LocalOutlierFactor
import numpy as np
import pickle

LOF_N_NEIGHBORS = 5

# TODO aca estoy perdiendo apreciacion
# quizas porque son floats, no se
training_cases = np.genfromtxt(
    "training_file_2.binetflow", delimiter=',', skip_header=True)

training_cases = training_cases[~np.isnan(training_cases).any(axis=1), :]

lof_novelty = LocalOutlierFactor(
    n_neighbors=LOF_N_NEIGHBORS, novelty=True).fit(training_cases)

# save model
model_file = open('model.pickle', 'wb')
pickle.dump(lof_novelty, model_file)
