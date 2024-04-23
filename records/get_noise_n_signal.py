import numpy as np
import sys, os
import _pickle as pickle
import matplotlib.pyplot as plt

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source folder', required=True)
args = parser.parse_args()

ret = os.system('clear')
if ret != 0:
    os.system('cls')

# ======================================================
MOD_LIST = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "BT-GFSK-S2Coding"]
TX_PWR_LIST = [str(x) for x in range(-20, 10, 5)]
# ======================================================
def load_pickle(filename):
    if not os.path.isfile(filename):
        print(f"{filename} is not exist.")
        exit()
    with open(filename, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data
    pass

def get_filenames_under_folder(tx_pwr):
    filename_list = []
    for mod in MOD_LIST:
        filename = f"{mod}.{tx_pwr}.236.dat"
        full_filename = f"{args.s}{filename}"
        if os.path.isfile(full_filename):
            filename_list.append(full_filename)
        else:
            print(f"{filename} is not a file.")
    return filename_list

def get_noise_signal(ary, spl_size=500, has_noise=False):
    abs_ary = np.abs(ary)

    threshold = (np.max(abs_ary) + np.mean(abs_ary))/2

    above_threshold = np.where(abs_ary > threshold)[0]

    
    if len(above_threshold) == 0:
        print("Threhold is invalid")
        return False, False
    
    valid_setting = True
    first_idx = above_threshold[0]
    if has_noise and first_idx-spl_size < 0:
        print("Not enough for noise")
        print(f"{first_idx-spl_size}:{first_idx} < 0")
        s_ret = ary[first_idx:first_idx+spl_size]
    else:
        s_ret = np.zeros((spl_size, ))

    if first_idx+spl_size > ary.shape[0]:
        print("Not enough for signal")
        print(f"{first_idx}:{first_idx+spl_size} > {ary.shape[0]}")
        n_ret = ary[first_idx-spl_size:first_idx]
    else:
        n_ret = np.zeros((spl_size, ))
    return s_ret, n_ret

# ======================================================
def main():
    
    for tx_pwr in TX_PWR_LIST:
        print("=="*10)
        file_list = get_filenames_under_folder(tx_pwr)
        dataset_dict = {}
        for filename in file_list:
            mod = filename.split('/')[2].split('.')[0]
            has_noise = False
            print('-'*20)
            print(f"{filename = }, {mod = }")
            record_data = np.fromfile(open(filename), dtype=np.complex64)

            # Range:
            # EIB_3F_hallway: 15_000:50_000
            # record_data = record_data[15_000:50_000]

            # EIB_outdoor: 30_000:70_000
            # record_data = record_data[30_000:70_000]

            # EIB_room_328_to_hallway: 30_000:70_000
            record_data = record_data[15_000:45_000]

            if filename.find("WIFI") > 0:
                has_noise = True
            signal, noise = get_noise_signal(record_data, has_noise=has_noise)

            dataset_dict[mod] = {
                'S': signal,
                'N': noise
            }

        fileprefix = args.s.split('/')[1]
        save_filename = f"./Dataset_signal_noise/{fileprefix}.{tx_pwr}.signal-noise.pkl"
        print(f"Save to {save_filename}")
        with open(save_filename, 'wb') as f:
            pickle.dump(dataset_dict, f)
        print(f"Done for power: {tx_pwr}")

    pass

if __name__ == "__main__":
    main()
