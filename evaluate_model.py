import train_model
import numpy as np
import pandas as pd
import common

INTRUSION_THRESHOLD = -1
INTRUSION = 'Y'
NOT_INTRUSION = 'N'
NEW_COLUMN_HEADER = f"IMT_MINDS ({NOT_INTRUSION}:{INTRUSION})"


def evaluate_model(training_file_path, test_file_path):
    model = train_model.train_model(training_file_path)

    test_cases = np.genfromtxt(
        test_file_path,
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

    df = pd.read_csv(test_file_path)
    df[NEW_COLUMN_HEADER] = predictions

    # add columns required by BotnetDetectorsComparer but that are not really used
    df['dur'] = df['runtime'] = df['proto'] = df['dir'] = df['state'] = df['sjit'] = df['djit'] = df['stos'] = df['dtos'] = df['pkts'] = df['bytes'] = df['trans'] = df['mean'] = df['stddev'] = df[
        'rate'] = df['sintpkt'] = df['sintdist'] = df['sintpktact'] = df['sintdistact'] = df['sintpktidl'] = df['sintdistidl'] = df['dintpkt'] = df['dintdist'] = df['dintpktact'] = df['dintdistact'] = df['dintpktidl'] = df['dintdistidl'] = None

    df = df.rename(columns={'StartTime': '#stime',
                            'SrcAddr': 'saddr', 'Sport': 'sport', 'DstAddr': 'daddr', 'Dport': 'dport'})

    df.to_csv("test_predictions.csv", index=False,
              columns=['#stime', 'dur', 'runtime', 'proto', 'saddr', 'sport', 'dir', 'daddr', 'dport', 'state', 'sjit', 'djit', 'stos', 'dtos', 'pkts', 'bytes', 'trans', 'mean', 'stddev', 'rate', 'sintpkt', 'sintdist', 'sintpktact', 'sintdistact', 'sintpktidl', 'sintdistidl', 'dintpkt', 'dintdist', 'dintpktact', 'dintdistact', 'dintpktidl', 'dintdistidl', 'Label', NEW_COLUMN_HEADER,
                       ])

    return df


def evaluate_model_and_print(training_file_path, test_file_path):
    df = evaluate_model(training_file_path, test_file_path)

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


if __name__ == "__main__":
    evaluate_model_and_print(
        "training_file_2.binetflow", "test_file_2.binetflow")
