import data_split
import evaluate_model
import common

print("Generating files")
training_df, testing_df = data_split.data_split_2format(
    "training_file.binetflow", "test_file.binetflow")

print("Training and evaluation model")
model, results = evaluate_model.evaluate_model_and_print(
    training_df[common.MODEL_COLUMNS].to_numpy(), testing_df
)
