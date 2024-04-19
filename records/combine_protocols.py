import numpy as np
import redis as redis
import json
import sys, os
import _pickle as pickle

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.')
parser.add_argument('-t', help='target npy file directory.')
parser.add_argument('-p', help='dataset pattern')
parser.add_argument('-i', help='Insepect the first 1_000_000 samples', default=False, action='store_true')
args = parser.parse_args()

mod_list = ["Trimmed-WIFI-BPSK", "Trimmed-WIFI-QPSK", "Trimmed-WIFI-16QAM", "Trimmed-WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "BT-GFSK-S8Coding"]
mod_real_name_list = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "BT-GFSK-S8Coding"]
mod_idx = [x for x in range(len(mod_list))]
mod_len = [1280, 880, 640, 560, 128, 128, 128, 128, 128]

ret = os.system('clear')
if ret != 0:
    os.system('cls')

# ------------------------------------------------

def is_all_file_exist():
    all_exist = True
    false_list = []
    for mod in mod_list:
        filename = f"{args.s}{mod}{args.p}dat"
        if not os.path.isfile(filename):
            all_exist = False
            false_list.append(filename)
    return all_exist, false_list
    pass

def main():
    print(f"{args = }")

    dataset_prefix = args.split("/")[1]
    all_exist, fail_list = is_all_file_exist()
    print(f"{all_exist = }, {fail_list = }")

    dataset_dict = {}
    for mod, mod_name, mod_i, mod_l in zip(mod_list, mod_real_name_list, mod_idx, mod_len):
        print("------------------------")
        src_filename = f"{args.s}{mod}{args.p}dat"
        record_data = np.fromfile(open(src_filename), dtype=np.complex64)

        print(f"{src_filename}, {record_data.shape = }")

        input_len = int(record_data.shape[0]/mod_l)

        _X_c = record_data.reshape((input_len, mod_l))
        _Y = np.array([mod_i for x in range(_X_c.shape[0])])

        _X_i = np.expand_dims(np.real(_X_c), axis=1)
        _X_q = np.expand_dims(np.imag(_X_c), axis=1)

        _X = np.concatenate((_X_i, _X_q), axis=1)


        dataset_dict[mod_name] = {
            "X": _X,
            "Y": _Y
            }


    print(f"{dataset_dict.keys() = }")
    save_filename = f"{args.s}{dataset_prefix}-protocol{args.p}pkl"
    print(f"Save to {save_filename}")
    pass

if __name__ == "__main__":
    invalid_input = False
    if args.s is None:
        print("Need source directory")
        invalid_input = True

    if args.p is None:
        print("Need pattern")
        invalid_input = True

    if invalid_input:
        exit()

    if args.t is None:
        args.t = args.s
    main()
