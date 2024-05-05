import numpy as np
import os, sys
import re
import matplotlib.pyplot as plt
from scipy.io import savemat
from scipy.io import loadmat

if os.system("clear") != 0:
    os.system("cls")

def main():

    BPSK_wave_dict = loadmat("BPSK_data_only.mat")
    QPSK_wave_dict = loadmat("QPSK_data_only.mat")
    QAM16_wave_dict = loadmat("16QAM_data_only.mat")
    QAM64_wave_dict = loadmat("64QAM_data_only.mat")

    BPSK_wave = BPSK_wave_dict["nonHT_BPSK_waveform"].astype(np.complex64)
    QPSK_wave = QPSK_wave_dict["nonHT_QPSK_waveform"].astype(np.complex64)
    QAM16_wave = QAM16_wave_dict["nonHT_16QAM_waveform"].astype(np.complex64)
    QAM64_wave = QAM64_wave_dict["nonHT_64QAM_waveform"].astype(np.complex64)

    BPSK_wave.tofile("BPSK_data_only.dat")
    QPSK_wave.tofile("QPSK_data_only.dat")
    QAM16_wave.tofile("16QAM_data_only.dat")
    QAM64_wave.tofile("64QAM_data_only.dat")
    pass

if __name__ == '__main__':
    main()