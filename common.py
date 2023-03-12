TRAINING_INDEXES = (0, 1, 2, 3, 4, 6, 7, 8, 9)
MODEL_COLUMNS = ['SrcAddr', 'DstAddr', 'Sport', 'Dport',
                 'Proto', 'count-dest', "count-src", "count-serv-src",
                 "count-serv-dest"]


def get_normal_and_background_indexes(df):
    return df["Label"].str.contains(
        "Background") | df["Label"].str.contains("Normal")
