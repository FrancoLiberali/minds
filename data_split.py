import pandas as pd
import ipaddress

TRAINING_SCENARIOS = [3, 4, 5, 7, 10, 11, 12, 13]
TEST_SCENARIOS = [1, 2, 6, 8, 9]


def ip_to_int(ip):
    try:
        return int(ipaddress.IPv4Address(ip))
    except:
        try:
            return int(ipaddress.IPv6Address(ip))
        except:
            return None


def create_training_file(file_name_list):
    full_training_file = pd.DataFrame()

    for file_name in file_name_list:
        print(file_name)
        scenario = pd.read_csv(
            file_name,
            usecols=['SrcAddr', 'DstAddr', 'Sport', 'Dport', 'Label']
        )

        # keep only flows with label Normal and Background
        scenario = scenario[
            scenario['Label'].str.contains(
                "Background") | scenario['Label'].str.contains("Normal")
        ]

        # map ip address to int
        scenario['SrcAddr'] = scenario[
            'SrcAddr'].apply(ip_to_int)
        scenario['DstAddr'] = scenario[
            'DstAddr'].apply(ip_to_int)

        # remove rows with null values
        scenario = scenario[
            scenario[
                ['SrcAddr', 'DstAddr', 'Sport', 'Dport']
            ].notnull().all(1)
        ]

        full_training_file = pd.concat(
            [full_training_file, scenario[['SrcAddr', 'DstAddr', 'Sport', 'Dport']]], ignore_index=True)
        del scenario

    full_training_file.to_csv("training_file.binetflow", index=False)
    return full_training_file


def data_split_2format():
    create_training_file(
        [f"{file_number}.binetflow.2format" for file_number in TRAINING_SCENARIOS])


data_split_2format()
