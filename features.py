from datetime import datetime, timedelta
import pandas as pd

T_WINDOW = 10  # seconds


def generate_time_window_features(df):
    df["StartTimeDatetime"] = pd.to_datetime(
        df['StartTime'],
        format="%Y/%m/%d %H:%M:%S.%f"
    )

    first_index = 0
    last_index = 0
    w_start_time = df.iloc[first_index]['StartTimeDatetime']

    final_df = pd.DataFrame()

    while first_index < len(df):
        w_finish_time = w_start_time + timedelta(seconds=T_WINDOW)

        last_index = df[
            df['StartTimeDatetime'] <= w_finish_time
        ].index.to_list()[-1]

        if last_index >= first_index:
            window_df = df.iloc[first_index: last_index + 1]

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

        first_index = last_index + 1
        w_start_time = w_finish_time

    final_df = final_df.drop("StartTimeDatetime", axis=1)
    return final_df
