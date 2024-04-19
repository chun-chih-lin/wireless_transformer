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
mod_idx = [x for x in range(len(mod_list))]

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

    all_exist, fail_list = is_all_file_exist()
    print(f"{all_exist = }, {fail_list = }")
    
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
