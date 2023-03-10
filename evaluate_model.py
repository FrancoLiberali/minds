import train_model
import numpy as np
import pandas as pd
import common

INTRUSION_THRESHOLD = -1
INTRUSION = 'Y'
NOT_INTRUSION = 'N'
NEW_COLUMN_HEADER = f"IMT_MINDS ({NOT_INTRUSION}:{INTRUSION})"


def evaluate_model():
    model = train_model.train_model("training_file_2.binetflow")

    test_cases = np.genfromtxt(
        "test_file_2.binetflow",
        delimiter=',',
        skip_header=True,
        usecols=(0, 1, 2, 3)
    )

    predictions = model.predict(test_cases)
    predictions = [INTRUSION if prediction <=
                   INTRUSION_THRESHOLD else NOT_INTRUSION for prediction in predictions]

    intrusion_amount = predictions.count(INTRUSION)
    print(f"Found {intrusion_amount} intrusions")

    del test_cases

    df = pd.read_csv("test_file_2.binetflow")
    df[NEW_COLUMN_HEADER] = predictions

    df.to_csv("test_predictions.csv", index=False)

    return df


if __name__ == "__main__":
    df = evaluate_model()

    is_normal_or_background = common.get_normal_and_background_indexes(df)
    is_predicted_intrusion = df[NEW_COLUMN_HEADER] == INTRUSION

    TN_amount = len(df[is_normal_or_background & ~is_predicted_intrusion])
    TP_amount = len(df[~is_normal_or_background & is_predicted_intrusion])
    FP_amount = len(df[is_normal_or_background & is_predicted_intrusion])
    FN_amount = len(df[~is_normal_or_background & ~is_predicted_intrusion])

    total_amount = len(df)

    print(f"TP: {TP_amount} / {total_amount}")
    print(f"TN: {TN_amount} / {total_amount}")
    print(f"FP: {FP_amount} / {total_amount}")
    print(f"FN: {FN_amount} / {total_amount}")
