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

def get_filenames_under_folder():
    filename_list = []
    for tx_pwr in TX_PWR_LIST:
        for mod in MOD_LIST:
            filename = f"{mod}.{tx_pwr}.236.dat"
            full_filename = f"{args.s}{filename}"
            if os.path.isfile(full_filename):
                filename_list.append(full_filename)
            else:
                print(f"{filename} is not a file.")
    return filename_list

def get_noise_signal(ary, threshold=0.25, spl_size=500, has_noise=False):
    print("-"*10)
    print(f"Getting noise")
    abs_ary = np.abs(ary)

    above_threshold = np.where(abs_ary > threshold)
    print(f"{above_threshold = }")
    print(f"{np.max(abs_ary) = }")
    print(f"{np.min(abs_ary) = }")
    print(f"{np.mean(abs_ary) = }")
    print(f"{np.median(abs_ary) = }")

    s_ret = np.zeros((spl_size, ))
    n_ret = np.zeros((spl_size, ))
    print(f"{ary.shape = }")


    plt.figure("signal")
    plt.plot(ary.real)
    plt.plot(ary.imag)
    plt.plot(np.abs(ary), linewidth=.5)
    # plt.axvline(above_threshold[0], color='r', linewidth=.5)
    return s_ret, n_ret

# ======================================================
def main():
    
    file_list = get_filenames_under_folder()
    for filename in file_list:
        has_noise = False
        print('-'*20)
        print(f"{filename = }")
        record_data = np.fromfile(open(filename), dtype=np.complex64)

        record_data = record_data[0:40_000]
        if filename.find("WIFI") > 0:
            print("Has noise")
            has_noise = True
        get_noise_signal(record_data, has_noise=has_noise)

        plt.show()
        break

    pass

if __name__ == "__main__":
    main()
