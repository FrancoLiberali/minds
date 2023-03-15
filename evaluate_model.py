import train_model
import numpy as np
import pandas as pd
import common

INTRUSION_THRESHOLD = -1
INTRUSION = 'Y'
NOT_INTRUSION = 'N'
NEW_COLUMN_HEADER = f"IMT_MINDS ({NOT_INTRUSION}:{INTRUSION})"


def evaluate_model(model, test_cases_df, predictions_file, intrusion_threshold=INTRUSION_THRESHOLD):
    test_cases = test_cases_df[common.MODEL_COLUMNS].to_numpy()
    # test_cases = test_cases[~np.isnan(test_cases).any(axis=1), :]

    predictions = model.predict(test_cases)
    predictions = [INTRUSION if prediction <=
                   intrusion_threshold else NOT_INTRUSION for prediction in predictions]

    intrusion_amount = predictions.count(INTRUSION)
    print(f"Found {intrusion_amount} intrusions")

    del test_cases

    df = test_cases_df
    df[NEW_COLUMN_HEADER] = predictions

    # add columns required by BotnetDetectorsComparer but that are not really used
    # df['dur'] = df['runtime'] = df['proto'] = df['dir'] = df['state'] = df['sjit'] = df['djit'] = df['stos'] = df['dtos'] = df['pkts'] = df['bytes'] = df['trans'] = df['mean'] = df['stddev'] = df[
    #     'rate'] = df['sintpkt'] = df['sintdist'] = df['sintpktact'] = df['sintdistact'] = df['sintpktidl'] = df['sintdistidl'] = df['dintpkt'] = df['dintdist'] = df['dintpktact'] = df['dintdistact'] = df['dintpktidl'] = df['dintdistidl'] = None

    # df = df.rename(columns={'StartTime': '#stime',
    #                         'SrcAddr': 'saddr', 'Sport': 'sport', 'DstAddr': 'daddr', 'Dport': 'dport'})

    # if predictions_file:
    #     df.to_csv(predictions_file, index=False,
    #               columns=[
    #                   '#stime', 'dur', 'runtime', 'proto', 'saddr', 'sport', 'dir', 'daddr', 'dport', 'state', 'sjit', 'djit', 'stos', 'dtos', 'pkts', 'bytes', 'trans', 'mean', 'stddev', 'rate', 'sintpkt', 'sintdist', 'sintpktact', 'sintdistact', 'sintpktidl', 'sintdistidl', 'dintpkt', 'dintdist', 'dintpktact', 'dintdistact', 'dintpktidl', 'dintdistidl', 'Label', NEW_COLUMN_HEADER,
    #               ])

    return df


def evaluate_model_and_print(model, test_cases_df, predictions_file):
    df = evaluate_model(model, test_cases_df, predictions_file)

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

    return df


if __name__ == "__main__":
    test_cases_df = pd.read_csv("test_file.binetflow",
                                dtype={'DstAddr': np.float64, 'SrcAddr': np.float64, 'Sport': np.int32, 'Dport': np.int32, 'Proto': np.int32,
                                       'count-dest': np.int32, 'count-src': np.int32, 'count-serv-src': np.int32, 'count-serv-dest': np.int32})

    training_cases = np.genfromtxt(
        "training_file.binetflow",
        delimiter=',',
        skip_header=True,
        usecols=common.TRAINING_INDEXES
    )

    model = train_model.train_model(training_cases)
    evaluate_model_and_print(model, test_cases_df, "test_predictions.csv")
