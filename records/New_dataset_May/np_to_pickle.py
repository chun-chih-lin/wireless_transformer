import numpy as np
import sys, os
import itertools
import _pickle as pickle

import argparse

parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.', required=True)
parser.add_argument('-y', help='Yes to all', default=False, action='store_true')
args = parser.parse_args()

if os.system('clear') != 0:
    os.system('cls')

MOD_LIST = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "BT-GFSK-S2Coding", "RAND"]
MOD_IDX = [x for x in range(len(MOD_LIST))]

TX_PWR = [-10, -5, 0, 5]
DIS = [5, 10, 15]
SAMP_RATE = [5, 20]
CF = 2360
INTER = [0, 1]

PKT_SIZE = 128
PKT_NUM = 20_000

# -------------------------------------------------
def get_filename(prefix, comb):
    mod_name = comb[0]
    tx_pwr = comb[1]
    dis = comb[2]
    samp_rate = comb[3]
    inter = comb[4]
    return f"{prefix}_{mod_name}_TP{tx_pwr}_D{dis}_SR{samp_rate}_CF{CF}_I{inter}.dat"

# -------------------------------------------------
def get_best(filename):
    data = np.fromfile(open(filename), dtype=np.complex64)
    print(f"{data.shape = }")
    n_pkt = int(data.shape[0]/PKT_SIZE)
    data = data.reshape((n_pkt, PKT_SIZE))
    mean_data = np.mean(data)
    print(f"{mean_data.shape = }")
    return data

def packet_to_pickle(prefix, tx_pwr, dis, samp_rate, inter):
    for (mod_name, mod_idx) in zip(MOD_LIST, MOD_IDX):
        filename = get_filename(prefix, [mod_name, tx_pwr, dis, samp_rate, inter])
        full_filename = f"{args.s}{filename}"
        best_data = get_best(full_filename)
        break
    pass

# -------------------------------------------------
def main():
    prefix = args.s.split('/')[1]

    combinations = itertools.product(MOD_LIST, TX_PWR, DIS, SAMP_RATE, INTER)

    check_succ = True

    for comb in combinations:
        filename = get_filename(prefix, list(comb))
        full_filename = f"{args.s}{filename}"
        if not os.path.exists(full_filename):
            print(f"{full_filename} Failed!")
            check_succ = False

    if not check_succ:
        exit()

    for inter in INTER:
        for dis in DIS:
            for samp_rate in SAMP_RATE:
                for tx_pwr in TX_PWR:
                    packet_to_pickle(prefix, tx_pwr, dis, samp_rate, inter)
                    exit()


if __name__ == '__main__':
    main()