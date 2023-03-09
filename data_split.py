import numpy as np
import pickle
import socket
import struct

# Split the dataset into training and test sets


def dataSplit(file3, file4, file5, file7, file11, file12, file13, testFile):
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


if __name__ == "__main__":
    dataSplit(r"/content/drive/MyDrive/Files/3.binetflow",
              r"/content/drive/MyDrive/Files/4.binetflow",
              r"/content/drive/MyDrive/Files/5.binetflow",
              r"/content/drive/MyDrive/Files/7.binetflow",
              r"/content/drive/MyDrive/Files/11.binetflow",
              r"/content/drive/MyDrive/Files/12.binetflow",
              r"/content/drive/MyDrive/Files/13.binetflow",
              r"/content/drive/MyDrive/Files/1.binetflow")
