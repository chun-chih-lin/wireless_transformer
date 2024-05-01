import numpy as np
import sys, os
import itertools
import _pickle as pickle

import argparse

parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.', required=True)
parser.add_argument('-y', help='Yes to all', default=False, action='store_true')
args = parser.parse_args()

MOD_LIST = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "BT-GFSK-S2Coding", "RAND"]
MOD_IDX = [x for x in range(len(MOD_LIST))]

TX_PWR = [-10, -5, 0, 5]
DIS = [5, 10, 15]
SAMP_RATE = [5, 20]
CF = 2360
INTER = [0, 1]

def get_filename(prefix, comb):
    
    mod_name = comb[0]
    tx_pwr = comb[1]
    dis = comb[2]
    samp_rate = comb[3]
    inter = comb[4]
    return f"{prefix}_{mod_name}_TP{tx_pwr}_D{dis}_SR{samp_rate}_CF{CF}_I{inter}.dat"

def main():
    prefix = args.s.split('/')[1]

    combinations = itertools.product(MOD_LIST, TX_PWR, DIS, SAMP_RATE, INTER)
    for comb in combinations:
        filename = get_filename(list(comb))
        full_filename = f"{args.s}{filename}"
        if os.path.exists(full_filename):
            print(f"{full_filename} Success!")
        else:
            print(f"{full_filename} Failed!")
    pass

if __name__ == '__main__':
    main()