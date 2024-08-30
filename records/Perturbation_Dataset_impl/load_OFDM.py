import numpy as np
import _pickle as pickle
import sys, os
import argparse

import matplotlib.pyplot as plt

from mapper import mapper
from matplotlib import pyplot as plt

if os.system("clear") != 0:
    os.system("cls")

packet_len = 3921

CLEAN_DATA_FILENAME="modulation_4_ori.pkl"
SAMPLE_LEN=20_000

data = np.fromfile(open('WiFi-BPSK.dat'), dtype=np.complex64)
# data = np.fromfile(open('WiFi-QPSK.dat'), dtype=np.complex64)
# data = np.fromfile(open('WiFi-16QAM.dat'), dtype=np.complex64)
# data = np.fromfile(open('WiFi-64QAM.dat'), dtype=np.complex64)

# data = np.fromfile(open('ori_Wi-Fi_BPSK.dat'), dtype=np.complex64)
# data = np.fromfile(open('ori_Wi-Fi_QPSK.dat'), dtype=np.complex64)
# data = np.fromfile(open('ori_Wi-Fi_16QAM.dat'), dtype=np.complex64)
# data = np.fromfile(open('ori_Wi-Fi_64QAM.dat'), dtype=np.complex64)

# data = np.fromfile(open('ch_Wi-Fi_BPSK.dat'), dtype=np.complex64)
# data = np.fromfile(open('ch_Wi-Fi_QPSK.dat'), dtype=np.complex64)
# data = np.fromfile(open('ch_Wi-Fi_16QAM.dat'), dtype=np.complex64)
# data = np.fromfile(open('ch_Wi-Fi_64QAM.dat'), dtype=np.complex64)


with open(CLEAN_DATA_FILENAME, 'rb') as f:
    data = pickle.load(f, encoding='latin1')
data_X = data['X']
data_X_c = np.squeeze(data_X[:, 0, :] + 1.0j*data_X[:, 1, :])
sub_data_fft = np.fft.fftshift(np.fft.fft(data_X_c[SAMPLE_LEN*0, :64]))
mapper.bpsk(sub_data_fft)

sub_data_fft = np.fft.fftshift(np.fft.fft(data_X_c[SAMPLE_LEN*1, :64]))
mapper.qpsk(sub_data_fft)

sub_data_fft = np.fft.fftshift(np.fft.fft(data_X_c[SAMPLE_LEN*2, :64]))
mapper.qam16(sub_data_fft)

sub_data_fft = np.fft.fftshift(np.fft.fft(data_X_c[SAMPLE_LEN*3, :64]))
int_array = mapper.qam64(sub_data_fft)

int_array = [1]
bit_array = mapper.int_array_to_bit_array(int_array, bit_num=1)
print(int_array)
print(f"{bit_array = }")

int_array = [3]
bit_array = mapper.int_array_to_bit_array(int_array, bit_num=2)
print(int_array)
print(f"{bit_array = }")

int_array = [12]
bit_array = mapper.int_array_to_bit_array(int_array, bit_num=4)
print(int_array)
print(f"{bit_array = }")

int_array = [64]
bit_array = mapper.int_array_to_bit_array(int_array, bit_num=6)
print(int_array)
print(f"{bit_array = }")