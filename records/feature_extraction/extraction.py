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
parser.add_argument('-s', '--source_folder', help='source torch experience file directory.', required=True)
parser.add_argument('-p', '--pattern', help='dataset pattern', required=True)

parser.add_argument('-t', '--tx_pwr', help='The transmission power(s)', default=5)
parser.add_argument('-d', '--distance', help='The distance(s)', default=15)
parser.add_argument('-r', '--samp_rate', help='The RX sample rate (in MHz)', default=20)
parser.add_argument('-i', '--interference', help='With/Without interference', default=0)

parser.add_argument('--inspect', help='inspect the result', action='store_true')
parser.add_argument('--plot_all', help='plot all results', action='store_true')
parser.add_argument('--plot_time', help='plot time results', action='store_true')
parser.add_argument('--plot_freq', help='plot freq results', action='store_true')

parser.add_argument('-y', help='yes to all', action='store_true')
args = parser.parse_args()

OUTDOOR_PREFIX="Dataset_EIB_Outdoor"
ROOM328_PREFIX="Dataset_EIB_room328_to_Hallway"
HALLWAY_PREFIX="Dataset_EIB_3F_Hallway_0430"
LINUX=0
WINDOWS=1

INSPECT = args.inspect
SHOW_FIG = args.plot_all
SHOW_TIME_FIG = SHOW_FIG or args.plot_time
SHOW_FREQ_FIG = SHOW_FIG or args.plot_freq

NUM_MOD_SAMPLE=20_000
SIZE_PER_DATA=128

TTL_N_MOD = 9
YES_FOR_ALL=False

MOD_NAME = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "Noise"]
MOD_COLOR=['tab:blue', 'tab:brown', 'tab:cyan', 'tab:green', \
           'tab:purple', 'tab:red', 'tab:pink', 'tab:orange', 'black']
# MOD_LINE=['', '', '', '', \
#           '', '', '', '']
LINEWIDTH=1.2

RAW_FEATURE_LABEL = 0
TIME_FEATURE_LABEL = 1
FREQ_FEATURE_LABEL = 2

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
    label = data['Y'][get_idx]
    print(f'{ret.shape = }')
    return ret, label

# Feature Extraction
def extract_features(data):
    # Main feature extraction code

    if False:
        process_ary, process_label = get_singla_data(data)
    else:
        process_ary = data['X']
        process_label = data['Y']

    # ----------------------------
    # show raw waveform
    # if False:
    #     for i in range(TTL_N_MOD):
    #         plt.plot(single_data[i, 0, :], 
    #             color=MOD_COLOR[i], 
    #             linewidth=LINEWIDTH, 
    #             label=MOD_NAME[i])
    #         plt.plot(single_data[i, 1, :], 
    #             color=MOD_COLOR[i], 
    #             linewidth=LINEWIDTH, 
    #             linestyle='-.')
    #     plt.legend(ncol=4, fontsize=7)
    #     plt.show()
    # ----------------------------
    
    print(f"{process_ary.shape = }")
    # 1. get the Time features
    time_indent = 64
    print("----------------------------")
    print("Time Feature Extraction")
    time_feature_ret = time_extraction(process_ary, indent=time_indent)
    time_feature_label = [TIME_FEATURE_LABEL for x in range(process_ary.shape[0])]
    if INSPECT:
        if time_feature_ret.shape[0] <= 20:
            inspect_time(time_feature_ret, process_label, MOD_NAME, show=SHOW_TIME_FIG)
            pass
        else:
            print("Too many reault. Skip plotting.")

    # 2. get the Freq features
    time_indent = 16
    N = 64
    freq_feature_ret = frequency_extraction(process_ary, N=N, indent=time_indent)
    freq_feature_label = [FREQ_FEATURE_LABEL for x in range(process_ary.shape[0])]

    if INSPECT:
        if freq_feature_ret.shape[0] <= 20:
            print(f"{freq_feature_ret.shape = }")
            inspect_freq(freq_feature_ret, process_label, MOD_NAME, show=SHOW_FREQ_FIG)
            pass
        else:
            print("Too many reault. Skip plotting.")

    # 3. packet to one file
    print("----------------------------")
    print(f"{time_feature_ret.shape = }, {freq_feature_ret.shape = }")
    X_shape = (process_ary.shape[0], 2, 128)
    print(f"{X_shape = }")
    time_feature_ret = time_feature_ret.reshape((X_shape))
    freq_feature_ret = freq_feature_ret.reshape((X_shape))

    # time_feature_ret = np.expand_dims(time_feature_ret, axis=1)
    # freq_feature_ret = np.expand_dims(freq_feature_ret, axis=1)

    process_ary_complex = np.expand_dims(process_ary[:, 0, :] + 1j*process_ary[:, 1, :], axis=1)
    print(f"{process_ary_complex.shape = }, {time_feature_ret.shape = }, {freq_feature_ret.shape = }")

    _X = np.concatenate((process_ary_complex, \
                         time_feature_ret, \
                         freq_feature_ret), axis=1)
    _X_i = _X.real.astype(np.float32)
    _X_q = _X.imag.astype(np.float32)
    print(f"{_X.shape = }, {_X_i.shape = }, {_X_q.shape = }")
    X = np.concatenate((_X_i, _X_q), axis=1)
    Y = process_label

    print(f"{X.shape = }, {Y.shape = }")

    dataset_dict = {
        'X': X,
        'Y': Y
    }

    save_pkl_name = f"{args.source_folder}{args.pattern}/{args.filename.split('.')[0]}-Time-Freq.pkl"
    save_flag = 'N'
    if not YES_FOR_ALL:
        save_flag = input(f"Confirm save to file {save_pkl_name}? [y/N]")

    if save_flag.upper() == "Y" or YES_FOR_ALL:
        with open(save_pkl_name, 'wb') as f:
            pickle.dump(dataset_dict, f)
        print(f"Saved to file: {save_pkl_name}")
    else:
        print("Abort.")
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
    args.filename = filename
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