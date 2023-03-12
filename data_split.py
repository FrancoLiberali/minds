import pandas as pd
import ipaddress
import common
import features

TRAINING_SCENARIOS = [3, 4, 5, 7, 10, 11, 12, 13]
TEST_SCENARIOS = [1, 2, 6, 8, 9]

LABEL_COLUMN = 'Label'
INTERESTING_COLUMNS = ['SrcAddr', 'DstAddr',
                       'Sport', 'Dport', 'Proto', LABEL_COLUMN, 'StartTime']
TRAINING_COLUMNS = ['SrcAddr', 'DstAddr',
                    'Sport', 'Dport', 'Proto', 'StartTime']
TESTING_COLUMNS = INTERESTING_COLUMNS

PROTOCOLS = ['tcp', 'udp', 'icmp', 'ipv6-icmp',
             'rtcp', 'rtp', 'udt', 'ipx/spx', 'arp',
             'esp', 'pim', 'igmp', 'unas', 'rarp', 'llc',
             'ipv6', 'rsvp']


def ip_to_int(ip):
    try:
        return int(ipaddress.IPv4Address(ip))
    except:
        try:
            return int(ipaddress.IPv6Address(ip))
        except:
            return None


def port_to_int(port):
    try:
        return int(port)
    except:
        try:
            return int(port, base=16)
        except:
            return 0


def protocol_to_int(protocol):
    return PROTOCOLS.index(protocol)


def concat_files(output_file_name, file_name_list, filter_botnet, columns_to_keep):
    concat_df = pd.DataFrame()

    for file_name in file_name_list:
        print(file_name)
        scenario = pd.read_csv(
            file_name,
            usecols=INTERESTING_COLUMNS
        )

        if filter_botnet:
            # keep only flows with label Normal and Background
            scenario = scenario[
                common.get_normal_and_background_indexes(scenario)
            ]

        # map ip address to int
        scenario['SrcAddr'] = scenario[
            'SrcAddr'].apply(ip_to_int)
        scenario['DstAddr'] = scenario[
            'DstAddr'].apply(ip_to_int)

        # map port to int (because icmp ports are in hexadecimal)
        scenario['Sport'] = scenario[
            'Sport'].apply(port_to_int)
        scenario['Dport'] = scenario[
            'Dport'].apply(port_to_int)

        # map protocol to int
        # print(scenario['Proto'].unique().tolist())
        scenario['Proto'] = scenario[
            'Proto'].apply(protocol_to_int)

        # remove rows with null values
        scenario = scenario[
            scenario[
                columns_to_keep
            ].notnull().all(1)
        ]

        concat_df = pd.concat(
            [concat_df, scenario[columns_to_keep]], ignore_index=True)
        del scenario

    concat_df = features.generate_time_window_features(concat_df)

    concat_df.to_csv(output_file_name, index=False)
    return concat_df


def data_split_2format():
    print("Creating training file")
    training_df = concat_files(
        "training_file.binetflow",
        [f"{file_number}.binetflow.2format" for file_number in TRAINING_SCENARIOS],
        True,
        TRAINING_COLUMNS,
    )

    print("Creating test file")
    testing_df = concat_files(
        "test_file.binetflow",
        [f"{file_number}.binetflow.2format" for file_number in TEST_SCENARIOS],
        False,
        TESTING_COLUMNS,
    )

    return training_df, testing_df


if __name__ == "__main__":
    data_split_2format()
