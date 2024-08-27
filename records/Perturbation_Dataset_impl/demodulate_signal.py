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

POSTFIX="TP-10_D5_SR20_CF2360_I0"

TARGET_MOD = "WIFI-BPSK"

# ---------------------------------------------------------------------
def load_npy(filename):
    return np.load(filename)

def load_dat(filename):
    return np.fromfile(open(filename), dtype=np.complex64)

def load_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data

def get_data(prefix, mod_name):
    # get clean data
    clean_data_name = f"{prefix}_{mod_name}_{POSTFIX}.pkl"
    clean_data_fulllname = os.path.join(prefix, clean_data_name)
    # get pert data
    pert_data_name = f"Non_process_{prefix}_pert_{mod_name}_{POSTFIX}.dat"
    pert_data_fulllname = os.path.join(f"{prefix}_pert", pert_data_name)

    clean_data = load_pickle(clean_data_fulllname)
    pert_data = load_dat(pert_data_fulllname)
    pert_data = pert_data.reshape((DATA_LEN, SAMPLE_LEN))
    clean_data_comple = clean_data[:, 0, :] + 1.0j*clean_data[:, 1, :]

    return clean_data_comple, pert_data

# ---------------------------------------------------------------------
def demod(mod_name, data):
    for sample_id in range(data.shape[0]):
        sample = data[sample_id, :]
        ret = 0
        if mod_name == "WIFI-BPSK":
            ret = demod_bpsk(sample)
        
        print(f"{ret = }")
        break
    pass

def demod_bpsk(data):
    # demodulating bpsk
    print(f"{data.shape = }")



# ---------------------------------------------------------------------
def main():
    for abbri, prefix in PREFIX.items():
        clean_data, pert_data = get_data(prefix, TARGET_MOD)

        print(f"{clean_data.shape = }")
        print(f"{pert_data.shape = }")

        accuracy = demod(TARGET_MOD, clean_data)
        break

    pass

# ---------------------------------------------------------------------
if __name__ == '__main__':
    main()