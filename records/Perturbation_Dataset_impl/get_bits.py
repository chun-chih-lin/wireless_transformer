import numpy as np
import _pickle as pickle
import sys, os
import argparse

from mapper import mapper
from matplotlib import pyplot as plt

if os.system("clear") != 0:
    os.system("cls")


BPSK_FILENAME="WiFi-BPSK.dat"
QPSK_FILENAME="WiFi-QPSK.dat"
QAM16_FILENAME="WiFi-16QAM.dat"
QAM64_FILENAME="WiFi-64QAM.dat"

FILENAMES=[BPSK_FILENAME, QPSK_FILENAME, QAM16_FILENAME, QAM64_FILENAME]
MOD_LIST=[2, 4, 16, 64]

LEN_PREAMPLE=160
LEN_TRAINING=160

SYMBOL_LEN=80
SYMBOL_CP=16

# ---------------------------------------------------------------------
def load_dat(filename):
    return np.fromfile(open(filename), dtype=np.complex64)

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

            plt.plot(fft_symbol.real, fft_symbol.imag, 'o')
            plt.show()
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
        cut_samples(data, mod)
        # break
    pass

if __name__ == '__main__':
    main()