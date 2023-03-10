import train_model
import numpy as np
import pandas as pd
import common

INTRUSION_THRESHOLD = -1

model = train_model.train_model("training_file_2.binetflow")

test_cases = np.genfromtxt(
    "test_file_2.binetflow",
    delimiter=',',
    skip_header=True,
    usecols=(0, 1, 2, 3)
)

predictions = model.predict(test_cases)
predictions = [common.INTRUSION if prediction <=
               INTRUSION_THRESHOLD else common.NOT_INTRUSION for prediction in predictions]

intrusion_amount = predictions.count(common.INTRUSION)
print(f"Found {intrusion_amount} intrusions")

del test_cases

df = pd.read_csv("test_file_2.binetflow")
df["Intrusion prediction"] = predictions

df.to_csv("test_predictions.csv", index=False)

TN_amount = len(df[(df["Label"] == common.NOT_INTRUSION) &
                (df["Intrusion prediction"] == common.NOT_INTRUSION)])
TP_amount = len(df[(df["Label"] == common.INTRUSION) &
                (df["Intrusion prediction"] == common.INTRUSION)])
FP_amount = len(df[(df["Label"] == common.NOT_INTRUSION) &
                (df["Intrusion prediction"] == common.INTRUSION)])
FN_amount = len(df[(df["Label"] == common.INTRUSION) &
                (df["Intrusion prediction"] == common.NOT_INTRUSION)])

total_amount = len(df)

print(f"TP: {TP_amount} / {total_amount}")
print(f"TN: {TN_amount} / {total_amount}")
print(f"FP: {FP_amount} / {total_amount}")
print(f"FN: {FN_amount} / {total_amount}")
