import numpy as np
import sys, os
import _pickle as pickle

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source folder', required=True)
parser.add_argument('-n', help='source pickle filename', required=True)
args = parser.parse_args()

ret = os.system('clear')
if ret != 0:
    os.system('cls')

# ======================================================
MOD_LIST = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "BT-GFSK-S2Coding"]
HAS_NOISE_LIST = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM"]
# ======================================================
def load_pickle(filename):
    if not os.path.isfile(filename):
        print(f"{filname} is not exist.")
        exit()
    with open(filename, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data
    pass

def get_noise_n_signal(ary, spl_size=500):
    sig = np.zeros((spl_size, ))
    noise = np.zeros((spl_size, ))
    print(f"{ary.shape = }")

    return sig, noise
    pass

# ======================================================
def main():
    data = load_pickle(f"{args.s}{args.n}")
    print(data.keys())
    for mod in MOD_LIST:
        print('-'*20)
        print(mod)
        sig, noise = get_noise_n_signal(data[mod]["X"])

    pass

if __name__ == "__main__":
    main()
