def get_normal_and_background_indexes(df):
    return df["Label"].str.contains(
        "Background") | df["Label"].str.contains("Normal")
