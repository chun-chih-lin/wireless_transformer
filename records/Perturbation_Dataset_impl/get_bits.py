import numpy as np
import _pickle as pickle
import sys, os
import argparse

from mapper import mapper
from matplotlib import pyplot as plt

if os.system("clear") != 0:
    os.system("cls")


BPSK_FILENAME="ch_Wi-Fi_BPSK.dat"
QPSK_FILENAME="ch_Wi-Fi_QPSK.dat"
QAM16_FILENAME="ch_Wi-Fi_16QAM.dat"
QAM64_FILENAME="ch_Wi-Fi_64QAM.dat"

# BPSK_FILENAME="ori_Wi-Fi_BPSK.dat"
# QPSK_FILENAME="ori_Wi-Fi_QPSK.dat"
# QAM16_FILENAME="ori_Wi-Fi_16QAM.dat"
# QAM64_FILENAME="ori_Wi-Fi_64QAM.dat"

FILENAMES=[BPSK_FILENAME, QPSK_FILENAME, QAM16_FILENAME, QAM64_FILENAME]
MOD_LIST=[2, 4, 16, 64]
LABEL_LIST=[0, 1, 2, 3]

LEN_PREAMPLE=160
LEN_TRAINING=160

SAMPLE_PKT=3921
SYMBOL_LEN=80
SYMBOL_CP=16

REMOVE_CP_IDX = [i for i in range(SYMBOL_CP, SYMBOL_LEN)] + [i for i in range(SYMBOL_CP+SYMBOL_LEN, 2*SYMBOL_LEN)]
# ---------------------------------------------------------------------
def load_dat(filename):
    return np.fromfile(open(filename), dtype=np.complex64)

def save_to_pickle(save_pkl_fullname, dataset_dict):
    with open(save_pkl_fullname, 'wb') as f:
        pickle.dump(dataset_dict, f)
    pass

def remove_headers(samples):
    ttl_pkts = samples.shape[0]//SAMPLE_PKT

    data_field = None
    for n_pkt in range(ttl_pkts):
        s_s = n_pkt*SAMPLE_PKT
        s_e = s_s + SAMPLE_PKT
        
        pkt_sample = np.expand_dims(samples[s_s+LEN_PREAMPLE+LEN_TRAINING:s_e-1], axis=0)

        if data_field is None:
            data_field = pkt_sample
        else:
            data_field = np.concatenate((data_field, pkt_sample), axis=0)
    # print(data_field.shape)

    ttl_pkt = data_field.shape[1]//160

    data_field = data_field[:, :ttl_pkt*SYMBOL_LEN*2]
    # print(data_field.shape, data_field[0, 16:16+10])
    data_field = data_field.reshape(data_field.shape[0], ttl_pkt, SYMBOL_LEN*2)
    # print(data_field.shape, data_field[0, 0, 16:16+10])
    data_field = data_field.reshape(data_field.shape[0]*ttl_pkt, SYMBOL_LEN*2)
    # print(data_field.shape, data_field[0, 16:16+10])

    data_field = data_field[:, REMOVE_CP_IDX]
    # print(data_field.shape, data_field[0, :10])


    data_field = np.concatenate((data_field, data_field[0:2, :]), axis=0)

    # data_field_r = np.expand_dims(data_field.real, axis=1)
    # data_field_i = np.expand_dims(data_field.imag, axis=1)

    # data_field_2d = np.concatenate((data_field_r, data_field_i), axis=1)
    # print(f"{data_field_2d.shape = }")

    return data_field


def cut_samples(samples, mod):
    data_field = samples[LEN_PREAMPLE+LEN_TRAINING:-1]
    num_samples = data_field.shape[0]
    num_symbols = num_samples//SYMBOL_LEN

    data_field = data_field.reshape((num_symbols, SYMBOL_LEN))

    for symbol_id, symbol in enumerate(data_field):
        if symbol_id >= 2:
            ori_symbol = symbol[SYMBOL_CP:]
            fft_symbol = np.fft.fftshift(np.fft.fft(ori_symbol))
            bits = symbol_to_bit(fft_symbol, mod)

            # plt.plot(fft_symbol.real, fft_symbol.imag, 'o')
            # plt.show()
            break

def symbol_to_bit(symbol, mod):
    if mod == 2:
        return mapper.bpsk(symbol)
    elif mod == 4:
        return mapper.qpsk(symbol)
    elif mod == 16:
        return mapper.qam16(symbol)
    elif mod == 64:
        return mapper.qam64(symbol)
    return False

def save_to_pickle(dat_file):
    pass

# ---------------------------------------------------------------------
def main():

    X, Y = None, None
    len_per_sample = 128

    for filename, mod, mod_i in zip(FILENAMES, MOD_LIST, LABEL_LIST):
        data = load_dat(filename)
        _X_c = remove_headers(data)
        print(_X_c.shape)

        _Y = np.array([mod_i for x in range(_X_c.shape[0])])

        _X_i = np.expand_dims(np.real(_X_c), axis=1)
        _X_q = np.expand_dims(np.imag(_X_c), axis=1)

        _X = np.concatenate((_X_i, _X_q), axis=1)

        if X is None and Y is None:
            X = _X
            Y = _Y
        else:
            X = np.concatenate((X, _X))
            Y = np.concatenate((Y, _Y))

    dataset_dict = {
        'X': X,
        'Y': Y
    }
    print(dataset_dict['X'].shape)
    print(dataset_dict['Y'].shape)

    save_pkl_fullname = f"modulation_4_wo_perturbation.pkl"
    print(f"{save_pkl_fullname = }")

    with open(save_pkl_fullname, 'wb') as f:
        pickle.dump(dataset_dict, f)
    pass

if __name__ == '__main__':
    main()