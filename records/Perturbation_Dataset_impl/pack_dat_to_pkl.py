import numpy as np
import _pickle as pickle
import sys, os
import argparse

import matplotlib.pyplot as plt

# from mapper import mapper
from matplotlib import pyplot as plt

if os.system("clear") != 0:
    os.system("cls")



ORI_BPSK_FILENAME="WiFi-BPSK.dat"
ORI_QPSK_FILENAME="WiFi-QPSK.dat"
ORI_QAM16_FILENAME="WiFi-16QAM.dat"
ORI_QAM64_FILENAME="WiFi-64QAM.dat"

# CH_BPSK_FILENAME="ch_Wi-Fi_BPSK.dat"
# CH_QPSK_FILENAME="ch_Wi-Fi_QPSK.dat"
# CH_QAM16_FILENAME="ch_Wi-Fi_16QAM.dat"
# CH_QAM64_FILENAME="ch_Wi-Fi_64QAM.dat"

BPSK_FILENAME="ori_Wi-Fi_BPSK.dat"
QPSK_FILENAME="ori_Wi-Fi_QPSK.dat"
QAM16_FILENAME="ori_Wi-Fi_16QAM.dat"
QAM64_FILENAME="ori_Wi-Fi_64QAM.dat"

ORI_FILENAMES=[ORI_BPSK_FILENAME, ORI_QPSK_FILENAME, ORI_QAM16_FILENAME, ORI_QAM64_FILENAME]

CH_FILENAME="modulation_4_wo_perturbation.pkl"
CH_FILENAME_01="modulation_4_wo_perturbation_n01.pkl"
CH_FILENAME_02="modulation_4_wo_perturbation_n02.pkl"
ORI_FILENAME="modulation_4_ori.pkl"

FILENAMES=[BPSK_FILENAME, QPSK_FILENAME, QAM16_FILENAME, QAM64_FILENAME]
MOD_LIST=[2, 4, 16, 64]
LABEL_LIST=[0, 1, 2, 3]

LEN_PREAMPLE=160
LEN_TRAINING=160
REMOVE_LAN=400

TTL_SAMPLE=20_000
SAMPLE_PKT=3921
SYMBOL_LEN=80
SYMBOL_CP=16

NOISE_AMP=0.2

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
        
        pkt_sample = np.expand_dims(samples[s_s+REMOVE_LAN:s_e-1], axis=0)

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

    data_field = data_field[:TTL_SAMPLE, REMOVE_CP_IDX]

    # data_field = np.concatenate((data_field, data_field[0:2, :]), axis=0)
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

def add_noise(data):
    print(data.shape)
    noise = np.random.normal(0, NOISE_AMP, size=data.shape) + 1.0j*np.random.normal(0, NOISE_AMP, size=data.shape)
    return data + noise

# ---------------------------------------------------------------------
def main():
    X, Y = None, None
    len_per_sample = 128

    plot_flag = True

    # for filename, mod, mod_i in zip(ORI_FILENAMES, MOD_LIST, LABEL_LIST):
    #     data = load_dat(filename)

    #     # if plot_flag:
    #     #     print(data.shape)
    #     #     symbol = data[320:320+80]
    #     #     print(symbol.shape)
    #     #     ori_symbol = symbol[SYMBOL_CP:]
    #     #     fft_symbol = np.fft.fftshift(np.fft.fft(ori_symbol))
    #     #     plt.plot(fft_symbol.real, fft_symbol.imag, 'o')
    #     #     plt.show()
    #     #     exit()

    #     plot_flag = False

    #     _X_c = remove_headers(data)
    #     print(_X_c.shape, np.max(np.abs(_X_c)))

    #     _Y = np.array([mod_i for x in range(_X_c.shape[0])])

    #     _X_i = np.expand_dims(np.real(_X_c), axis=1)
    #     _X_q = np.expand_dims(np.imag(_X_c), axis=1)

    #     _X = np.concatenate((_X_i, _X_q), axis=1)

    #     if X is None and Y is None:
    #         X = _X
    #         Y = _Y
    #     else:
    #         X = np.concatenate((X, _X))
    #         Y = np.concatenate((Y, _Y))

    # dataset_dict = {
    #     'X': X,
    #     'Y': Y
    # }
    # print(dataset_dict['X'].shape)
    # print(dataset_dict['Y'].shape)

    # with open(ORI_FILENAME, 'wb') as f:
    #     pickle.dump(dataset_dict, f)
    

    # =================================================================
    X, Y = None, None
    plot_flag = True
    for filename, mod, mod_i in zip(ORI_FILENAMES, MOD_LIST, LABEL_LIST):
        data = load_dat(filename)

        _X_c_ori = remove_headers(data)
        _X_c = add_noise(_X_c_ori)

        # if plot_flag:
        #     print(_X_c.shape)
        #     symbol_ori = _X_c_ori[0, :64]
        #     symbol = _X_c[0, :64]
        #     print(symbol.shape)
        #     # ori_symbol_ori = symbol_ori[SYMBOL_CP:]
        #     fft_symbol_ori = np.fft.fftshift(np.fft.fft(symbol_ori))

        #     # ori_symbol = symbol[SYMBOL_CP:]
        #     fft_symbol = np.fft.fftshift(np.fft.fft(symbol))

        #     plt.plot(fft_symbol_ori.real, fft_symbol_ori.imag, 'rx')
        #     plt.plot(fft_symbol.real, fft_symbol.imag, 'o')
        #     plt.show()

        print(_X_c.shape, np.max(np.abs(_X_c)))

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

    with open(CH_FILENAME_02, 'wb') as f:
        pickle.dump(dataset_dict, f)
    pass

if __name__ == '__main__':
    main()