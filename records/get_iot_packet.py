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
def get_packets(ary, filename, pkt_size=500, mov_wdw_s=100):
    abs_ary = np.abs(ary)
    n_ary = ary.shape[0]

    mov_wdw = np.ones((mov_wdw_s, ))
    mov_avg = np.zeros(ary.shape)

    mov_avg = np.convolve(abs_ary, mov_wdw/mov_wdw_s)

    max_v = np.max(mov_avg)

    mov_avg_threshold = (np.max(mov_avg) + np.mean(mov_avg)*9)/10
    above_threshold = np.where(mov_avg > mov_avg_threshold)[0]
    above_list = np.array([1 if x > mov_avg_threshold else 0 for x in mov_avg])

    raising_detect = np.where(above_list[1:] - above_list[:-1] == 1)[0] - int(mov_wdw_s/2)
    falling_detect = np.where(above_list[1:] - above_list[:-1] == -1)[0] - int(mov_wdw_s/2)

    if falling_detect[0] < raising_detect[0]:
        falling_detect.pop(0)

    if len(falling_detect) != len(raising_detect):
        raising_detect = raising_detect[:len(falling_detect)]

    packet_len = falling_detect - raising_detect
    min_packet_len = np.min(packet_len)
    print(f"{min_packet_len = }")

    x_p = [x+int(mov_wdw_s/2) for x in range(n_ary)]

    if len(above_threshold) == 0:
        print("Threhold is invalid")
        return None

    pkt_ret = None
    if INSPECT:
        print(f"{raising_detect = }")
        above_list = above_list*0.8*max_v
        plt.plot(ary.real, linewidth=0.5)
        plt.plot(ary.imag, linewidth=0.5)
        plt.plot(abs_ary, linewidth=0.5)
        plt.axhline(np.max(mov_avg), color='k', linestyle='-.', linewidth=0.5)
        plt.axhline(np.mean(mov_avg), color='k', linestyle='-.', linewidth=0.5)
        plt.axhline(mov_avg_threshold, color='k', linewidth=0.7)
        plt.plot(x_p, mov_avg[mov_wdw_s-1:], color='b', linewidth=0.7)
        plt.plot(x_p, above_list[mov_wdw_s-1:], color='r', linewidth=0.7)
        for (raise_d, fall_d) in zip(raising_detect, falling_detect):
            plt.axvline(raise_d, color='r', linestyle='-.', linewidth=0.7)
            plt.axvline(fall_d, color='r', linestyle=':', linewidth=0.7)
        plt.title(filename)
        plt.show()

    for raise_d in raising_detect:
        if min_packet_len > pkt_size:
            min_packet_len = pkt_size

        if raise_d+min_packet_len > n_ary:
            break
            
        pkt = np.expand_dims(ary[raise_d:raise_d+min_packet_len], axis=0)
        if pkt_ret is None:
            pkt_ret = pkt
        else:
            pkt_ret = np.concatenate((pkt_ret, pkt), axis=0)

    return pkt_ret
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
            data = data[500_000:600_000]

        packets = get_packets(data, filename)
        if not INSPECT and packets is None:
            print(f"Processe {full_filename} failed. Not packet detected.")
            continue

        n_pkt = packets.shape[0]
        print(f"{packets.shape = }")
        print(f"Number of packet: {n_pkt}")
    pass

if __name__ == '__main__':
    main()