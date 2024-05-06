import numpy as np
import os, sys
import _pickle as pickle
import matplotlib.pyplot as plt
import math

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source folder.', required=True)
parser.add_argument('-p', help='source pattern.', required=True)
parser.add_argument('-i', help='inspect mode.', default=False, action='store_true')
args = parser.parse_args()


INSPECT = args.i
MOD_LIST = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "BT-GFSK-S8Coding"]
BATCH_SIZE=100_000_000
MAX_PACKET=10_000

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
def get_packets(ary, filename, pkt_size=500, mov_wdw_s=10):
    abs_ary = np.abs(ary)
    n_ary = ary.shape[0]

    mov_wdw = np.ones((mov_wdw_s, ))
    mov_avg = np.zeros(ary.shape)

    mov_avg = np.convolve(abs_ary, mov_wdw/mov_wdw_s)

    max_v = np.max(mov_avg)

    mov_avg_threshold = (np.max(mov_avg) + np.mean(mov_avg)*9)/10
    above_threshold = np.where(mov_avg > mov_avg_threshold)[0]
    if len(above_threshold) == 0:
        print("=============== Threhold is invalid ===============")
        return []

    above_list = np.array([1 if x > mov_avg_threshold else 0 for x in mov_avg])

    raising_detect = np.where(above_list[1:] - above_list[:-1] == 1)[0] - int(mov_wdw_s/2)
    falling_detect = np.where(above_list[1:] - above_list[:-1] == -1)[0] - int(mov_wdw_s/2)

    if falling_detect[0] < raising_detect[0]:
        falling_detect.pop(0)

    if len(falling_detect) != len(raising_detect):
        raising_detect = raising_detect[:len(falling_detect)]

    if raising_detect[0] <= int(mov_wdw_s/2):
        raising_detect = raising_detect[1:]
        falling_detect = falling_detect[1:]

    if falling_detect[-1] >= n_ary-int(mov_wdw_s/2):
        raising_detect = raising_detect[:-1]
        falling_detect = falling_detect[:-1]

    to_remove = []
    for i, (raise_d, fall_d) in enumerate(zip(raising_detect, falling_detect)):
        if fall_d - raise_d < 100:
            to_remove.append(i)

    raising_detect = np.delete(raising_detect, to_remove)
    falling_detect = np.delete(falling_detect, to_remove)
    
    packet_len = falling_detect - raising_detect
    if len(packet_len) == 0:
        print("=============== Not detecting any packet ===============")
        return []

    min_packet_len = np.min(packet_len)

    x_p = [x+int(mov_wdw_s/2) for x in range(n_ary)]
    
    print(f"{len(raising_detect) = }, {min_packet_len = }")
    if INSPECT:
        # print(f"{raising_detect = }")
        # print(f"{falling_detect = }")
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

    pkt_ret = None
    if min_packet_len > pkt_size:
        min_packet_len = pkt_size
    
    pkt_i = 0
    for raise_d in raising_detect:
        pkt_i += 1
        if raise_d+min_packet_len > n_ary:
            break

        pkt = np.expand_dims(ary[raise_d:raise_d+min_packet_len], axis=0)
        # print(f"{pkt.shape = }")
        if pkt_ret is None:
            pkt_ret = pkt
        else:
            pkt_ret = np.concatenate((pkt_ret, pkt), axis=0)

        if pkt_i >= MAX_PACKET:
            break

    return pkt_ret
    pass

# ==========================================================

def main():
    filename_list = get_filename_list()
    for filename in filename_list:
        print("-"*25)
        print("-"*25)
        filename_prefix = ".".join(filename.split('.')[:-1])
        full_filename = f"{args.s}{filename}"
        if not os.path.exists(full_filename):
            print(f"{full_filename} is not a file.")
            continue

        print(f"Processing {full_filename}...")
        data = load_dat_from_file(full_filename)
        if INSPECT:
            data = data[20_000_000:30_000_000]

        n_batch = math.ceil(data.shape[0]/BATCH_SIZE)
        print(f"Total batches: {n_batch}, Total sample: {data.shape}")

        for n_b in range(n_batch):
            save_batch_packets_name = f"{args.s}packets/B{n_b+1}-{n_batch}_{filename_prefix}.pkl"
            
            if os.path.exists(save_batch_packets_name):
                print(f"File {save_batch_packets_name} exists. Skip")
                break

            print("-"*10)
            print(f"[{n_b+1}/{n_batch}]")
            print(f"{n_b*BATCH_SIZE = }, {(n_b+1)*BATCH_SIZE = }")
            if (n_b+1)*BATCH_SIZE >= data.shape[0]:
                process_data = data[n_b*BATCH_SIZE:]
            else:
                process_data = data[n_b*BATCH_SIZE:(n_b+1)*BATCH_SIZE]

            print(f"{process_data.shape = }")
            packets = get_packets(process_data, filename)
            if packets is None:
                print("Packet is None")
                continue
            if len(packets) == 0:
                print("Can not get any packets.")
                continue
            if not INSPECT and packets is None:
                print(f"Processe {full_filename} failed. Not packet detected.")
                continue

            n_pkt = packets.shape[0]
            print(f"Number of packet: {packets.shape[0]}, length: {packets.shape[1]}")
            
            print(f"{save_batch_packets_name = }")
            packets.tofile(save_batch_packets_name)
            if n_pkt >= MAX_PACKET:
                break
    pass

if __name__ == '__main__':
    main()