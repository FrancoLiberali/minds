import data_split
import evaluate_model
import common
import train_model

print("Generating files")
training_df, testing_df = data_split.data_split_2format(
    "training_file.binetflow", "test_file.binetflow")

print("Training and evaluation model")
model = train_model.train_model(training_df[common.MODEL_COLUMNS].to_numpy())
results = evaluate_model.evaluate_model_and_print(
    model, testing_df, "test_predictions.csv"
)
