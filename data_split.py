import pandas as pd
import numpy as np
import pickle
import socket
import struct

# Split the dataset into training and test sets


def data_split(file3, file4, file5, file7, file11, file12, file13, testFile):
    files = [file3, file4, file5, file7, file11, file12, file13]
    data = data2 = ""
    for file in files:
        with open(file) as fp:
            data2 = fp.read()
            data += data2
    fileName = 'fichier_3_4_5_7_10_11_12_13_fusionne_entrainement.binetflow'
    with open(fileName, 'w') as fp:
        fp.write(data)
    f = open(fileName, 'r')
    # Training data
    x = []
    y = []
    # Test data
    xT = []
    yT = []
    # Put the normal training flows in variables in order to perform the novelty detection
    for packet in f:
        pfields = packet[:-1].split(',')
        Sport, Dport, SrcAddr, DstAddr, label = pfields[4], pfields[7], pfields[3], pfields[6], pfields[-1]
        try:
            Sip = socket.inet_aton(SrcAddr)
            Sip = struct.unpack("!L", Sip)[0]
        except:
            continue
        try:
            Dip = socket.inet_aton(DstAddr)
            Dip = struct.unpack("!L", Dip)[0]
        except:
            continue
        if Sport == '':
            continue
        if Dport == '':
            continue
        #back, nor, bot
        try:

            if "Background" in label:
                label = 0

            elif "Normal" in label:
                label = 0

            elif "Botnet" in label:
                label = 1

            # Training Dataset
            # Its a Normal dataset, doesn't contain bots
            if label == 0:
                x.append([int(Sport), int(Dport), Sip, Dip])
                y.append(label)
            else:
                continue
        except:
            continue

    # Prepare the testfile in a suitable format for the BOtnetComparer code
    g = open(testFile, 'r')
    line = ''
    pckt_type = ''
    line1 = '#stime,dur, runtime, proto, saddr, sport, dir, daddr, dport, state, sjit, djit, stos, dtos, pkts, bytes, trans, mean, stddev, rate, sintpkt, sintdist, sintpktact, sintdistact, sintpktidl, sintdistidl, dintpkt, dintdist, dintpktact, dintdistact, dintpktidl, dintdistidl, Label(Normal:CC) ,MINDS(Normal:CC)'
    test_list = []
    test_list.append(line1)

    for packet in g:
        pfields = packet[:-1].split(',')
        stime, dur, runtime, proto, Sport, dir, Dport, SrcAddr, DstAddr,  totP, label = pfields[0], pfields[1], pfields[
            1], pfields[2], pfields[4], pfields[5], pfields[7], pfields[3], pfields[6], pfields[-4], pfields[-1]
        try:
            Sip = socket.inet_aton(SrcAddr)
            Sip = struct.unpack("!L", Sip)[0]
        except:
            continue

        try:
            Dip = socket.inet_aton(DstAddr)
            Dip = struct.unpack("!L", Dip)[0]
        except:
            continue

        if Sport == '':
            continue
        if Dport == '':
            continue
        #back, nor, bot
        try:
            if "Background" in label:
                label = 0
                pckt_type = 'flow=Normal'

            elif "Normal" in label:
                label = 0
                pckt_type = 'flow=Normal'

            elif "Botnet" in label:
                label = 1
                pckt_type = 'flow=CC'

            xT.append([int(Sport), int(Dport), Sip, Dip])
            yT.append(label)

            line = str(stime) + ','+str(dur)+','+str(runtime)+','+str(proto)+','+str(SrcAddr)+','+str(Sport)+',' + \
                str(dir)+','+str(DstAddr)+','+str(Dport)+','+',,,,,' + \
                str(totP)+',,,,,,,,,,,,,,,,,,'+str(pckt_type)
            test_list.append(line)
        except:
            continue

    # pickle the dataset for fast loading
    file = open('flowdata.pickle', 'wb')
    pickle.dump([np.array(x), np.array(y), np.array(xT), np.array(yT)], file)

    file_test = open('file_test.pickle', 'wb')
    pickle.dump(test_list, file_test)

    # return the training and the test dataset
    return np.array(x), np.array(y), np.array(xT), np.array(yT)


TRAINING_SCENARIOS = [3, 4, 5, 7, 10, 11, 12, 13]
TEST_SCENARIOS = [1, 2, 6, 8, 9]


def concat_files(file_name, file_name_list):
    full_training_file = pd.DataFrame()

    for file_name in file_name_list:
        scenario = pd.read_csv(file_name, usecols=[
            'SrcAddr', 'DstAddr', 'Sport', 'Dport', 'Label'])

        # keep only flows with label Normal and Background
        scenario[scenario['Label'].str.contains(
            "Background") | scenario['Label'].str.contains("Normal")]

        full_training_file = pd.concat(
            [full_training_file, scenario[['SrcAddr', 'DstAddr', 'Sport', 'Dport']]], ignore_index=True)
        del scenario

    full_training_file.to_csv(file_name)
    return full_training_file


def data_split_2format():
    concat_files("training_file.binetflow", [
                 f"{file_number}.binetflow.2format" for file_number in TRAINING_SCENARIOS])


data_split_2format()
