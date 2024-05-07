import numpy as np
import os, sys
import _pickle as pickle
import matplotlib.pyplot as plt

from time import process_time

from frequency_extraction import frequency_extraction
from frequency_extraction import inspect_freq

from time_extraction import time_extraction
from time_extraction import inspect_time

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', '--source_folder', help='source torch experience file directory.')
parser.add_argument('-p', '--pattern', help='dataset pattern')

parser.add_argument('-t', '--tx_pwr', help='The transmission power(s)', default=5)
parser.add_argument('-d', '--distance', help='The distance(s)', default=15)
parser.add_argument('-r', '--samp_rate', help='The RX sample rate (in MHz)', default=20)
parser.add_argument('-i', '--interference', help='With/Without interference', default=0)

parser.add_argument('-y', help='yes to all', action='store_true')
args = parser.parse_args()

OUTDOOR_PREFIX="Dataset_EIB_Outdoor"
ROOM328_PREFIX="Dataset_EIB_room328_to_Hallway"
HALLWAY_PREFIX="Dataset_EIB_3F_Hallway_0430"
LINUX=0
WINDOWS=1

NUM_MOD_SAMPLE=20_000
SIZE_PER_DATA=128

TTL_N_MOD = 9

MOD_NAME = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "Noise"]
MOD_COLOR=['tab:blue', 'tab:brown', 'tab:cyan', 'tab:green', \
           'tab:purple', 'tab:red', 'tab:pink', 'tab:orange', 'black']
# MOD_LINE=['', '', '', '', \
#           '', '', '', '']
LINEWIDTH=1.2

OS_SYS = LINUX
if os.name == "nt":
    OS_SYS = WINDOWS

if os.system("clear") != 0:
    os.system("cls")

# =================================================
def get_singla_data(data):
    indent = 10
    get_idx = [x*NUM_MOD_SAMPLE+indent for x in range(TTL_N_MOD)]
    ret = data['X'][get_idx, :, :]
    print(f'{ret.shape = }')
    return ret

# Feature Extraction
def extract_features(data):
    # Main feature extraction code
    single_data = get_singla_data(data)
    # plt.plot(single_data[-1, 0, :], 
    #     color=MOD_COLOR[-1], 
    #     linewidth=LINEWIDTH, 
    #     label=MOD_NAME[-1])
    # plt.plot(single_data[-1, 1, :], 
    #     color=MOD_COLOR[-1], 
    #     linewidth=LINEWIDTH, 
    #     linestyle='-.')
    # plt.show()

    # ----------------------------
    # show raw waveform
    if False:
        for i in range(TTL_N_MOD):
            plt.plot(single_data[i, 0, :], 
                color=MOD_COLOR[i], 
                linewidth=LINEWIDTH, 
                label=MOD_NAME[i])
            plt.plot(single_data[i, 1, :], 
                color=MOD_COLOR[i], 
                linewidth=LINEWIDTH, 
                linestyle='-.')
        plt.legend(ncol=4, fontsize=7)
        plt.show()
    # ----------------------------

    # 1. get the Time features


    # 2. get the Freq features



    pass

# =================================================
# Getting data
def load_pickle_from_file(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data

def get_data(args):
    filename = f"{args.pattern}_TP{args.tx_pwr}_D{args.distance}_SR{args.samp_rate}_CF2360_I{args.interference}.pkl"
    full_filename = f"{args.source_folder}{args.pattern}/{filename}"
    print(f"{full_filename = }")
    if not os.path.exists(full_filename):
        print("File does not exist")
        exit()

    print("File exists")
    return load_pickle_from_file(full_filename)

# =================================================
def main():
    print(args)
    if args.pattern == "O":
        args.pattern = OUTDOOR_PREFIX
    elif args.pattern == "R":
        args.pattern = ROOM328_PREFIX
    elif args.pattern == "H":
        args.pattern = HALLWAY_PREFIX

    data = get_data(args)
    
    extract_features(data)
    pass

if __name__ == '__main__':
    main()