from sklearn.neighbors import LocalOutlierFactor
import numpy as np
import pickle
import common

LOF_N_NEIGHBORS = 5


def train_model(training_cases, save_model=False):
    training_cases = training_cases[~np.isnan(training_cases).any(axis=1), :]

    lof_novelty = LocalOutlierFactor(
        n_neighbors=LOF_N_NEIGHBORS, novelty=True
    ).fit(training_cases)

    if save_model:
        model_file = open('model.pickle', 'wb')
        pickle.dump(lof_novelty, model_file)

    return lof_novelty


if __name__ == "__main__":
    training_cases = np.genfromtxt(
        "training_file.binetflow",
        delimiter=',',
        skip_header=True,
        usecols=common.TRAINING_INDEXES
    )

    train_model(training_cases)
