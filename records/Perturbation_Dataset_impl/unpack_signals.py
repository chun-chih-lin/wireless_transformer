import numpy as np
import _pickle as pickle
import sys, os
import argparse

if os.system("clear") != 0:
    os.system("cls")

# ---------------------------------------------------------------------
MOD_LIST = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", \
            "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", \
            "BT-GFSK-S2Coding", "RAND"]
MOD_IDX = [x for x in range(len(MOD_LIST))]

DATA_LEN = 20_000
SAMPLE_LEN = 128

OUTDOOR_PREFIX="Dataset_EIB_Outdoor"
ROOM328_PREFIX="Dataset_EIB_room328_to_Hallway"
HALLWAY_PREFIX="Dataset_EIB_3F_Hallway"
PREFIX = {
    "O": OUTDOOR_PREFIX,
    "R": ROOM328_PREFIX,
    "H": HALLWAY_PREFIX
}
ALL_IN_ONE_POSTFIX="TP-10_D5_SR20_CF2360_I0.pkl"

# ---------------------------------------------------------------------
def load_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data

def save_as_pkl(filename, data_dict):
    with open(filename, 'wb') as f:
        pickle.dump(data_dict, f)
    pass

# ---------------------------------------------------------------------
def main():
    print(MOD_LIST, len(MOD_LIST))

    for abbri, prefix in PREFIX.items():
        print(prefix)
        filename = os.path.join(prefix, f"{prefix}_{ALL_IN_ONE_POSTFIX}")
        print(os.path.exists(filename))
        data = load_pickle(filename)
        print(data["X"].shape)

        for mod_i, mod in enumerate(MOD_LIST):
            print(mod_i*DATA_LEN, (mod_i+1)*DATA_LEN)
            save_filename = f"{prefix}_{mod}_{ALL_IN_ONE_POSTFIX}"
            
            save_full_filename = os.path.join(prefix, save_filename)

            mod_data = data["X"][mod_i*DATA_LEN:(mod_i+1)*DATA_LEN]
            mod_label = data["Y"][mod_i*DATA_LEN:(mod_i+1)*DATA_LEN]

            print(f"{save_full_filename = }")
            print(f"{mod_data.shape}, {mod_label}")
            # save_as_pkl(save_full_filename, mod_data)
            # break
        # break
    pass

if __name__ == '__main__':
    main()
