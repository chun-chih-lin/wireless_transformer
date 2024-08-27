import numpy as np
import _pickle as pickle
import sys, os
import argparse

if os.system("clear") != 0:
    os.system("cls")


BPSK_FILENAME="Wi-Fi_BPSK.dat"
QPSK_FILENAME="Wi-Fi_QPSK.dat"
QAM16_FILENAME="Wi-Fi_16QAM.dat"
QAM64_FILENAME="Wi-Fi_64QAM.dat"

FILENAMES=[BPSK_FILENAME, QPSK_FILENAME, QAM16_FILENAME, QAM64_FILENAME]

LEN_PREAMPLE=160
LEN_TRAINING=160

# ---------------------------------------------------------------------
def load_dat(filename):
    return np.fromfile(open(filename), dtype=np.complex64)

def cut_samples(samples):
    print(f"{samples.shape = }")
    samples = samples[LEN_PREAMPLE+LEN_TRAINING:]
    print(f"{samples.shape = }")
    num_samples = samples.shape[0]
    print(f"{num_samples//64} {(num_samples//64)*64}, {num_samples = }")

# ---------------------------------------------------------------------
def main():

    for filename in FILENAMES:
        data = load_dat(filename)
        cut_samples(data)

    pass

if __name__ == '__main__':
    main()