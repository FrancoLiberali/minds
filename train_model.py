from sklearn.neighbors import LocalOutlierFactor
import numpy as np
import pickle

LOF_N_NEIGHBORS = 5

TRAINING_INDEXES = (0, 1, 2, 3, 4, 6, 7)


def train_model(training_file_name, save_model=False):
    training_cases = np.genfromtxt(
        training_file_name,
        delimiter=',',
        skip_header=True,
        usecols=TRAINING_INDEXES
    )

    training_cases = training_cases[~np.isnan(training_cases).any(axis=1), :]

    lof_novelty = LocalOutlierFactor(
        n_neighbors=LOF_N_NEIGHBORS, novelty=True).fit(training_cases)

    if save_model:
        model_file = open('model.pickle', 'wb')
        pickle.dump(lof_novelty, model_file)

    return lof_novelty


if __name__ == "__main__":
    train_model("training_file_2.binetflow")
