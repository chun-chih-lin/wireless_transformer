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
ORI_DATA_FILENAME="modulation_4_ori.pkl"

PERT_DATA_FILENAME="modulation_4_w_perturbation.npy"
PERT_DATA_INDEX="modulation_4_w_perturbation_index.npy"

# PERT_DATA_FILENAME="modulation_4_w_perturbation_0.1.npy"
# PERT_DATA_INDEX="modulation_4_w_perturbation_0.1_index.npy"

# PERT_DATA_FILENAME="modulation_4_w_perturbation_0.5.npy"
# PERT_DATA_INDEX="modulation_4_w_perturbation_0.5_index.npy"

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

with open(ORI_DATA_FILENAME, 'rb') as f:
    data = pickle.load(f, encoding='latin1')
ori_data = data['X']

pert_data_idx =np.load(PERT_DATA_INDEX)
pert_data =np.load(PERT_DATA_FILENAME)
print(pert_data.shape)

print(sys.argv[1])
symbol_idx = int(sys.argv[1])
print(f"{symbol_idx = }, {type(symbol_idx)}")
true_idx = pert_data_idx[symbol_idx]

ori_symbol = ori_data[true_idx, 0, :64] + 1.0j*ori_data[true_idx, 1, :64]
one_symbol = pert_data[symbol_idx, 0, :64] + 1.0j*pert_data[symbol_idx, 1, :64]

print(f"{true_idx = } {true_idx//20_000}")

ori_symbol_fft = np.fft.fftshift(np.fft.fft(ori_symbol))
one_symbol_fft = np.fft.fftshift(np.fft.fft(one_symbol))
plt.plot(one_symbol_fft.real, one_symbol_fft.imag, 'bo')
plt.plot(ori_symbol_fft.real, ori_symbol_fft.imag, 'rx')
plt.show()
exit()

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