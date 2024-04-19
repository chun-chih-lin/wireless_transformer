import numpy as np
import os, sys
import matplotlib.pyplot as plt
import _pickle as pickle

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.')
parser.add_argument('-t', help='target npy file directory.')
parser.add_argument('-i', help='inspect result', default=False, action='store_true')
args = parser.parse_args()

if os.system('clear') != 0:
    os.system('cls')

INSPECT = args.i
print(f"{INSPECT = }")


# ----------------------------------------------------
def get_mod_list():
    if args.s.find("protocol") > 0:
        dataset_type = "protocol"
        mod_list = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "BT-GFSK-S2Coding"]
    else:
        dataset_type = "simple"
        mod_list = ["BPSK", "QPSK", "8PSK", "QAM16", "QAM64", "AM-DSB", "AM-SSB", "PAM4", "CPFSK", "GFSK", "WBFM", "RAND"]
        # mod_idx = [x for x in range(len(mod_list))]
    return mod_list, dataset_type

# ----------------------------------------------------
def main():
    print(args.s)
    mod_list, dataset_type = get_mod_list()

    if not os.path.exists(args.s):
        print(f"{args.s} is not a valid file")
        exit()

    with open(args.s, 'rb') as f:
        all_data = pickle.load(f, encoding='latin1')

    print(dataset_type)
    if dataset_type == "simple":
        print(all_data.keys())
        X = all_data["X"]
        print(f"{X.shape = }")
    else:
        print(all_data.keys())
        for key in all_data.keys():
            X = all_data[key]["X"]
            print(f"{key}, {X.shape = }")
            


    
    pass

if __name__ == '__main__':
    invalid_input = False
    if args.s is None:
        print("Need source pkl file")
        invalid_input = True

    if invalid_input:
        exit()

    if args.t is None:
        args.t = args.s
    main()