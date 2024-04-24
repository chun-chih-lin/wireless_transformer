import numpy as np
import os, sys
import _pickle as pickle
import matplotlib.pyplot as plt

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source folder.', required=True)
parser.add_argument('-p', help='source pattern.', required=True)
parser.add_argument('-i', help='inspect mode.', default=False, action='store_true')
args = parser.parse_args()


INSPECT = args.i
MOD_LIST = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "BT-GFSK-S2Coding"]

if os.system("clear") != 0:
    os.system("cls")

# ==========================================================
def load_dat_from_file(full_filename):
    return np.fromfile(open(full_filename), dtype=np.complex64)

def load_pickle_from_file():
    with open(args.s, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data

def files_under_folder(folder):
    return os.listdir(folder)

def get_filename_list():
    filenames = files_under_folder(args.s)
    filelist = []
    for filename in filenames:
        if filename.find(args.p) >= 0:
            filelist.append(filename)
    return filelist

# ==========================================================
def get_packets(ary, pkt_size=500, mov_wdw_s=100):
    abs_ary = np.abs(ary)

    mov_wdw = np.ones((mov_wdw_s, ))
    mov_avg = np.zeros(ary.shape)

    mov_avg = np.convolve(abs_ary, mov_wdw/mov_wdw_s)

    max_v = np.max(mov_avg)

    mov_avg_threshold = (np.max(mov_avg) + np.mean(mov_avg))/2
    above_threshold = np.where(mov_avg > mov_avg_threshold)[0]
    above_list = [0.8*max_v if x > mov_avg_threshold else 0 for x in mov_avg]

    if len(above_threshold) == 0:
        print("Threhold is invalid")
        return None

    pkt_ret = None
    print(f"{above_threshold = }")

    plt.plot(ary.real)
    plt.plot(ary.imag)
    plt.plot(abs_ary)
    plt.axhline(mov_avg_threshold, color='y', linewidth=0.5)
    plt.plot(above_list, color='r', linewidth=0.5)


    pass

# ==========================================================
def main():

    filename_list = get_filename_list()
    for filename in filename_list:
        print("-"*25)
        full_filename = f"{args.s}{filename}"
        if not os.path.exists(full_filename):
            print(f"{full_filename} is not a file.")
            continue

        print(f"Processing {full_filename}...")
        data = load_dat_from_file(full_filename)

        if INSPECT:
            data = data[0:100_000]

        packets = get_packets(data)
        if not INSPECT and packets is None:
            print(f"Processe {full_filename} failed. Not packet detected.")
            continue

        if INSPECT:
            plt.show()

        n_pkt = packets.shape[0]
        print(f"Number of packet: {n_pkt}")

        break
    pass

if __name__ == '__main__':
    main()