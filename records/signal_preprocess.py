import numpy as np
import os, sys
import matplotlib.pyplot as plt
import _pickle as pickle

from time import process_time

from frequency_extraction import frequency_extraction
from frequency_extraction import inspect_freq

from time_extraction import time_extraction
from time_extraction import inspect_time

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.', required=True)
parser.add_argument('-n', help='source pkl filename.', required=True)
parser.add_argument('-i', help='inspect result', default=False, action='store_true')
parser.add_argument('-p', help='plot all result', default=False, action='store_true')
parser.add_argument('-t', help='plot time result', default=False, action='store_true')
parser.add_argument('-f', help='plot freq result', default=False, action='store_true')
args = parser.parse_args()

if os.system('clear') != 0:
    os.system('cls')

INSPECT = args.i
SHOW_FIG = args.p
SHOW_TIME_FIG = SHOW_FIG or args.t
SHOW_FREQ_FIG = SHOW_FIG or args.f

RAW_FEATURE_LABEL = 0
TIME_FEATURE_LABEL = 1
FREQ_FEATURE_LABEL = 2

SAMPLE_PRE_MOD = 20_000
SUB_SAMPLE_PRE_MOD = 10_000

print(f"{INSPECT = }")

# ----------------------------------------------------
def get_mod_list():
    if args.n.find("protocol") > 0:
        dataset_type = "protocol"
        mod_list = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "BT-GFSK-S2Coding"]
    else:
        dataset_type = "simple"
        mod_list = ["BPSK", "QPSK", "8PSK", "QAM16", "QAM64", "AM-DSB", "AM-SSB", "PAM4", "CPFSK", "GFSK", "WBFM", "RAND"]
        # mod_idx = [x for x in range(len(mod_list))]
    return mod_list, dataset_type

def get_sub_ary(process_ary, process_label):
    num_sec = int(process_ary.shape[0]/SAMPLE_PRE_MOD)
    process_ary_shape = list(process_ary.shape)
    process_ary_shape[0] = int(num_sec*SUB_SAMPLE_PRE_MOD)
    process_ary_shape = tuple(process_ary_shape)
    print(f"{process_ary_shape = }, {process_ary_shape[0]}, {num_sec = }")

    ret_ary = np.zeros(process_ary_shape)
    ret_label = np.zeros((process_ary_shape[0], ))
    for i in range(num_sec):
        s = i*SAMPLE_PRE_MOD
        e = s + SUB_SAMPLE_PRE_MOD
        ret_ary[i*SUB_SAMPLE_PRE_MOD:(i+1)*SUB_SAMPLE_PRE_MOD, :, :] = process_ary[s:e, :, :]
        ret_label[i*SUB_SAMPLE_PRE_MOD:(i+1)*SUB_SAMPLE_PRE_MOD] = process_label[s:e]
    return ret_ary, ret_label

# ----------------------------------------------------
def main():
    print(args.s)
    t1_start = process_time() 
    mod_list, dataset_type = get_mod_list()
    print(f"{mod_list}: {dataset_type = }")
    filename = f"{args.s}{args.n}"
    if not os.path.exists(filename):
        print(f"{filename} is not a valid file")
        exit()
    with open(filename, 'rb') as f:
        all_data = pickle.load(f, encoding='latin1')

    process_ary = all_data['X']
    process_label = all_data['Y']

    # process_ary, process_label = get_sub_ary(process_ary, process_label)
 
    if INSPECT:
        process_idx = [5, 20_005, 40_005, 60_005, \
                  80_005, 100_005, 120_005, 140_005, \
                  160_005, 180_005, 200_005]
        # process_idx = [x for x in range(20_000)]
        # process_idx = [100_001]
        process_ary = process_ary[process_idx, :, :]
        process_label = process_label[process_idx].astype(int)


    # ==========================================
    # Time Feature Extraction
    time_indent = 64
    print("----------------------------")
    print("Time Feature Extraction")
    time_feature_ret = time_extraction(process_ary, indent=time_indent)
    time_feature_label = [TIME_FEATURE_LABEL for x in range(process_ary.shape[0])]
    if INSPECT:
        if time_feature_ret.shape[0] <= 20:
            inspect_time(time_feature_ret, process_label, mod_list, show=SHOW_TIME_FIG)
            pass
        else:
            print("Too many reault. Skip plotting.")

    # ==========================================
    # Frequency Feature Extraction
    # Getting the Frequency Feature Extraction result and label.
    time_indent = 16
    print("----------------------------")
    print("Frequency Feature Extraction")
    freq_feature_ret = frequency_extraction(process_ary, indent=time_indent)
    freq_feature_label = [FREQ_FEATURE_LABEL for x in range(process_ary.shape[0])]

    if INSPECT:
        if freq_feature_ret.shape[0] <= 20:
            inspect_freq(freq_feature_ret, process_label, mod_list, show=SHOW_FREQ_FIG)
            pass
        else:
            print("Too many reault. Skip plotting.")
    # ==========================================

    print("----------------------------")
    t1_stop = process_time() 
    print("Elapsed time during the whole program in seconds:", t1_stop - t1_start)

    if INSPECT:
        exit()

    print("----------------------------")
    _X = np.concatenate((np.expand_dims(time_feature_ret, axis=1), np.expand_dims(freq_feature_ret, axis=1)), axis=1)
    _X_i = _X.real
    _X_q = _X.imag
    print(f"{_X.shape = }, {_X_i.shape = }, {_X_q.shape = }")
    X = np.concatenate((_X_i, _X_q), axis=1)
    Y = process_label

    print(f"{X.shape = }, {Y.shape = }")

    dataset_dict = {
        'X': X,
        'Y': Y
    }

    save_pkl_name = f"{args.s}{args.n.split('.')[0]}-Time-Freq.pkl"
    save_flag = input(f"Confirm save to file {save_pkl_name}? [y/N]")
    if save_flag.upper() == "Y":
        with open(save_pkl_name, 'wb') as f:
            pickle.dump(dataset_dict, f)
        print(f"Saved to file: {save_pkl_name}")
    else:
        print("Abort.")
    pass


if __name__ == '__main__':
    invalid_input = False
    if args.s is None:
        print("Need source pkl file")
        invalid_input = True

    if invalid_input:
        exit()
    main()