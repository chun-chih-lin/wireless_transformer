import numpy as np
import _pickle as pickle
import sys, os
import argparse

import matplotlib.pyplot as plt

from mapper import mapper
from matplotlib import pyplot as plt

if os.system("clear") != 0:
    os.system("cls")


CH_BPSK_FILENAME="ch_Wi-Fi_BPSK.dat"
CH_QPSK_FILENAME="ch_Wi-Fi_QPSK.dat"
CH_QAM16_FILENAME="ch_Wi-Fi_16QAM.dat"
CH_QAM64_FILENAME="ch_Wi-Fi_64QAM.dat"

ORI_BPSK_FILENAME="ori_Wi-Fi_BPSK.dat"
ORI_QPSK_FILENAME="ori_Wi-Fi_QPSK.dat"
ORI_QAM16_FILENAME="ori_Wi-Fi_16QAM.dat"
ORI_QAM64_FILENAME="ori_Wi-Fi_64QAM.dat"

ORI_DATA_FILENAME="modulation_4_ori.pkl"
CLEAN_DATA_FILENAME="modulation_4_wo_perturbation.pkl"
PERT_DATA_FILENAME="modulation_4_w_perturbation.npy"
PERT_DATA_INDEX="modulation_4_w_perturbation_index.npy"

CH_FILENAMES=[CH_BPSK_FILENAME, CH_QPSK_FILENAME, CH_QAM16_FILENAME, CH_QAM64_FILENAME]
ORI_FILENAMES=[ORI_BPSK_FILENAME, ORI_QPSK_FILENAME, ORI_QAM16_FILENAME, ORI_QAM64_FILENAME]
MOD_LIST=[2, 4, 16, 64]
LABEL_LIST=[0, 1, 2, 3]

OFDM_SYMBOL_LEN=64

# ---------------------------------------------------------------------
def get_index():
    return list(np.load(PERT_DATA_INDEX))

def get_clean_data():
    index = get_index()
    with open(CLEAN_DATA_FILENAME, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data['X'][index, :, :], data['Y'][index]

def get_pert_data():
    return np.load(PERT_DATA_FILENAME)
    
def get_ori_data():
    index = get_index()
    with open(ORI_DATA_FILENAME, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data['X'][index, :, :]

def fft(symbol):
    return np.fft.fftshift(np.fft.fft(symbol))

# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
def calculate_ber(ori_data, clean_data, pert_data, label):
    print(f"{label = }")
    ori_sym = ori_data[:64]
    clean_sym = clean_data[:64]
    pert_sym = pert_data[:64]

    ori_fft = fft(ori_sym)
    clean_fft = fft(clean_sym)
    pert_fft = fft(pert_sym)


    # plt.plot(ori_fft.real, ori_fft.imag, 'o')
    plt.plot(clean_fft.real, clean_fft.imag, '^')
    plt.plot(pert_fft.real, pert_fft.imag, '*')
    plt.show()


    if label == 0:
        # BPSK
        mapper.bpsk(ori_sym)
        pass
    elif label == 1:
        # QPSK
        mapper.qpsk(ori_sym)
        pass
    elif label == 2:
        # 16QAM
        mapper.qam16(ori_sym)
        pass
    else:
        # 64QAM
        mapper.qam64(ori_sym)
        pass
    pass

# ---------------------------------------------------------------------
def main():
    ori_data_collection = get_ori_data()
    pert_data_collection = get_pert_data()
    clean_data_collection, data_label = get_clean_data()

    print(f"{ori_data_collection.shape = }")
    print(f"{pert_data_collection.shape = }")
    print(f"{clean_data_collection.shape = }")
    print(f"{data_label.shape = }")
    print(data_label)



    for pkt_i, label in enumerate(data_label):
        if not label == 0:
            continue

        ori_data = ori_data_collection[pkt_i, 0, :] + 1.0j*ori_data_collection[pkt_i, 1, :]
        pert_data = pert_data_collection[pkt_i, 0, :] + 1.0j*pert_data_collection[pkt_i, 1, :]
        clean_data = clean_data_collection[pkt_i, 0, :] + 1.0j*clean_data_collection[pkt_i, 1, :]
        calculate_ber(ori_data, clean_data, pert_data, label)
        break
    pass

# ---------------------------------------------------------------------
if __name__ == '__main__':
    main()