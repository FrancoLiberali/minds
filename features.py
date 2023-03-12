from datetime import datetime, timedelta
import pandas as pd

T_WINDOW = 60  # seconds


def generate_time_window_features(df):
    print("Generating time window features")
    df["StartTimeDatetime"] = pd.to_datetime(
        df['StartTime'],
        format="%Y/%m/%d %H:%M:%S.%f"
    )

    first_index = 0
    last_index = 0
    w_start_time = df.iloc[first_index]['StartTimeDatetime']

    rows_amount = len(df)

    final_df = pd.DataFrame()

    last_percentage = 0
    print("0%")

    while first_index < rows_amount:
        percentage = (first_index * 100) // rows_amount
        if percentage >= last_percentage + 5:
            print(f"{percentage}%")
            last_percentage = percentage

        w_finish_time = w_start_time + timedelta(seconds=T_WINDOW)

        resting_df = df.iloc[first_index:]

        last_index = resting_df[
            'StartTimeDatetime'
        ].searchsorted(w_finish_time)

        if last_index == 0:
            # if the window is empty go directly to the window starting in the first element
            w_start_time = resting_df.iloc[0]['StartTimeDatetime']
        else:
            last_index = first_index + last_index
            window_df = df.iloc[first_index: last_index]

            # count-dest
            window_df = window_df.join(
                window_df.groupby(
                    ['SrcAddr']
                )['DstAddr'].nunique().rename("count-dest"),
                on=['SrcAddr']
            )

            # count-src
            window_df = window_df.join(
                window_df.groupby(
                    ['DstAddr']
                )['SrcAddr'].nunique().rename("count-src"),
                on=['DstAddr']
            )

            # count-serv-src
            window_df = window_df.join(
                window_df.groupby(
                    ['SrcAddr', 'Dport']
                ).size().rename("count-serv-src"),
                on=['SrcAddr', 'Dport']
            )

            # count-serv-dest
            window_df = window_df.join(
                window_df.groupby(
                    ['DstAddr', 'Sport']
                ).size().rename("count-serv-dest"),
                on=['DstAddr', 'Sport']
            )

            final_df = pd.concat([final_df, window_df], ignore_index=True)
            first_index = last_index

        w_start_time = w_finish_time

    final_df = final_df.drop("StartTimeDatetime", axis=1)
    return final_df
