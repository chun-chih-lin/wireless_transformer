import numpy as np
import sys, os
import itertools
import _pickle as pickle
import gzip
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

def get_pickle_filename(prefix, tx_pwr, dis, samp_rate, inter):
    return f"{prefix}_TP{tx_pwr}_D{dis}_SR{samp_rate}_CF{CF}_I{inter}.pkl"

# -------------------------------------------------
def get_best(filename):
    data = np.fromfile(open(filename), dtype=np.complex64)
    n_pkt = int(data.shape[0]/PKT_SIZE)
    data = data.reshape((n_pkt, PKT_SIZE))
    mean_data = np.mean(data, axis=1)
    
    if mean_data.shape[0] == PKT_NUM:
        return data

    idx_list = [x for x in range(mean_data.shape[0])]

    best_idx = [x for _, x in sorted(zip(mean_data, idx_list))]
    best_idx = best_idx[0:PKT_NUM]
    return data[best_idx, :]

def packet_to_pickle(prefix, tx_pwr, dis, samp_rate, inter):
    pickle_name = get_pickle_filename(prefix, tx_pwr, dis, samp_rate, inter)
    full_pickle_name = f"{args.s}{pickle_name}"
    if os.path.exists(full_pickle_name):
        print(f"{full_pickle_name} already exits. Abort.")
        return full_pickle_name

    X, Y = None, None
    for (mod_name, mod_idx) in zip(MOD_LIST, MOD_IDX):
        filename = get_filename(prefix, [mod_name, tx_pwr, dis, samp_rate, inter])
        full_filename = f"{args.s}{filename}"
        _X_c = get_best(full_filename)
        print(f"{_X_c.shape = }")

        _Y = np.array([mod_idx for x in range(_X_c.shape[0])])
        _X_i = np.expand_dims(np.real(_X_c), axis=1)
        _X_q = np.expand_dims(np.imag(_X_c), axis=1)
        _X = np.concatenate((_X_i, _X_q), axis=1)

        print(f"Save {mod_name} with label: {mod_idx}. Data size: {_X.shape}, label size: {_Y.shape}")

        if X is None and Y is None:
            X = _X
            Y = _Y
        else:
            X = np.concatenate((X, _X))
            Y = np.concatenate((Y, _Y))

    dataset_dict = {
        "X": X,
        "Y": Y
    }
    print(f"Total data size: {dataset_dict['X'].shape}")
    print(f"Total label size: {dataset_dict['Y'].shape}")
    
    print(f"Will be Saved to pickle file: {full_pickle_name}")

    input_cmd = "N"
    if not args.y:
        input_cmd = input("Is everything looking right and confirm save to file? [y/N]")

    if input_cmd.upper() == "Y" or args.y:
        print("Saving...")
        with open(full_pickle_name, 'wb') as f:
            pickle.dump(dataset_dict, f)
        print("Saved.")
    else:
        print("Abort.")
    return full_pickle_name

def pack_to_tar_gz(prefix, full_list_of_file):
    tar_filename = f"{prefix}.tar"
    full_tar_filename = {args.s}{tar_filename}
    tar_cmd = f"tar -cvf {full_tar_filename}"
    
    full_list = " ".join(full_list_of_file)

    cmd = f"{tar_cmd} {full_list}"
    print(f"{cmd = }")
    # Pack into a tar file
    os.system(cmd)
    
    # compress to a gzip file
    gz_cmd = f"gzip {full_tar_filename}"
    os.system(gz_cmd)
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

    ttl_full_pickle_name = []
    for inter in INTER:
        for dis in DIS:
            for samp_rate in SAMP_RATE:
                for tx_pwr in TX_PWR:
                    print('\n------------------------------')
                    full_pickle_name = packet_to_pickle(prefix, tx_pwr, dis, samp_rate, inter)
                    ttl_full_pickle_name.append(full_pickle_name)
    pack_to_tar_gz(prefix, ttl_full_pickle_name)


if __name__ == '__main__':
    main()