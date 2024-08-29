import numpy as np
import _pickle as pickle
import sys, os
import argparse

from mapper import mapper
from matplotlib import pyplot as plt

if os.system("clear") != 0:
    os.system("cls")


BPSK_FILENAME="Wi-Fi_BPSK.dat"
QPSK_FILENAME="Wi-Fi_QPSK.dat"
QAM16_FILENAME="Wi-Fi_16QAM.dat"
QAM64_FILENAME="Wi-Fi_64QAM.dat"

FILENAMES=[BPSK_FILENAME, QPSK_FILENAME, QAM16_FILENAME, QAM64_FILENAME]
MOD_LIST=[2, 4, 16, 64]

LEN_PREAMPLE=160
LEN_TRAINING=160

SAMPLE_PKT=3921
SYMBOL_LEN=80
SYMBOL_CP=16

REMOVE_CP_IDX = [i for i in range(SYMBOL_CP, SYMBOL_LEN)] + [i for i in range(SYMBOL_CP+SYMBOL_LEN, 2*SYMBOL_LEN)]
# ---------------------------------------------------------------------
def load_dat(filename):
    return np.fromfile(open(filename), dtype=np.complex64)

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
    print(data_field.shape)

    ttl_pkt = data_field.shape[1]//160

    data_field = data_field[:, :ttl_pkt*SYMBOL_LEN*2]
    print(data_field.shape, data_field[0, 16:16+10])
    data_field = data_field.reshape(data_field.shape[0], ttl_pkt, SYMBOL_LEN*2)
    print(data_field.shape, data_field[0, 0, 16:16+10])
    data_field = data_field.reshape(data_field.shape[0]*ttl_pkt, SYMBOL_LEN*2)
    print(data_field.shape, data_field[0, 16:16+10])

    data_field = data_field[:, REMOVE_CP_IDX]
    print(data_field.shape, data_field[0, :10])

    data_field_r = np.expand_dims(data_field.real, axis=1)
    data_field_i = np.expand_dims(data_field.imag, axis=1)

    data_field_2d = np.concatenate((data_field_r, data_field_i), axis=1)
    print(f"{data_field_2d.shape = }")

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

# ---------------------------------------------------------------------
def main():

    for filename, mod in zip(FILENAMES, MOD_LIST):
        data = load_dat(filename)
        remove_headers(data)
        # cut_samples(data, mod)
        break
    pass

if __name__ == '__main__':
    main()