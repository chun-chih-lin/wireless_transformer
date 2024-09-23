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
CLEAN_01_DATA_FILENAME="modulation_4_wo_perturbation_n01.pkl"
CLEAN_02_DATA_FILENAME="modulation_4_wo_perturbation_n02.pkl"

# PERT_DATA_FILENAME="modulation_4_w_perturbation.npy"
# PERT_DATA_INDEX="modulation_4_w_perturbation_index.npy"

# PERT_DATA_FILENAME="modulation_4_w_perturbation_0.1.npy"
# PERT_DATA_INDEX="modulation_4_w_perturbation_0.1_index.npy"

# PERT_DATA_FILENAME="modulation_4_w_perturbation_0.5.npy"
# PERT_DATA_INDEX="modulation_4_w_perturbation_0.5_index.npy"

PERT_DATA_FILENAME="modulation_4_w_perturbation_clip_0.5.npy"
PERT_DATA_INDEX="modulation_4_w_perturbation_clip_0.5_index.npy"

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
    with open(CLEAN_01_DATA_FILENAME, 'rb') as f:
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
def int_to_bit_array(num, num_bit=1):
    ret = []
    if num_bit == 1:
        for bit in f'{num:01b}':
            ret.append(bit)
    elif num_bit == 2:
        for bit in f'{num:02b}':
            ret.append(bit)
    elif num_bit == 4:
        for bit in f'{num:04b}':
            ret.append(bit)
    elif num_bit == 6:    
        for bit in f'{num:06b}':
            ret.append(bit)
    return ret

def int_array_to_bit_array(main_array, sec_arr, thr_arr, num_bit=1):
    main_ret, sec_ret, thr_ret = [], [], []
    for (num, sec, thr) in zip(main_array, sec_arr, thr_arr):
        if num is None or sec is None or thr is None:
            continue

        num_bit_ary = int_to_bit_array(num, num_bit=num_bit)
        sec_bit_ary = int_to_bit_array(sec, num_bit=num_bit)
        thr_bit_ary = int_to_bit_array(thr, num_bit=num_bit)

        main_ret = main_ret + num_bit_ary
        sec_ret = sec_ret + sec_bit_ary
        thr_ret = thr_ret + thr_bit_ary

    return main_ret, sec_ret, thr_ret

def compare_bits(truth, compare):
    num_bit = len(truth)
    num_correct = 0

    ret = [1 if t == c else 0 for (t, c) in zip(truth, compare)]
    return num_bit, np.sum(ret)

# ---------------------------------------------------------------------
def calculate_ber(ori_data, clean_data, pert_data, label):
    ori_sym = ori_data[:64]
    clean_sym = clean_data[:64]
    pert_sym = pert_data[:64]

    ori_fft = fft(ori_sym)
    clean_fft = fft(clean_sym)
    pert_fft = fft(pert_sym)

    if label == 0:
        num_bit = 1
    elif label == 1:
        num_bit = 2
    elif label == 2:
        num_bit = 4
    elif label == 3:
        num_bit = 6

    if label == 0:
        # BPSK
        ground_truth_decode_sym = mapper.bpsk(ori_fft)
        chan_decode_sym = mapper.bpsk(clean_fft)
        pert_decode_sym = mapper.bpsk(pert_fft)
    elif label == 1:
        # QPSK
        ground_truth_decode_sym = mapper.qpsk(ori_fft)
        chan_decode_sym = mapper.qpsk(clean_fft)
        pert_decode_sym = mapper.qpsk(pert_fft)
    elif label == 2:
        # 16QAM
        ground_truth_decode_sym = mapper.qam16(ori_fft)
        chan_decode_sym = mapper.qam16(clean_fft)
        pert_decode_sym = mapper.qam16(pert_fft)
    else:
        # 64QAM
        ground_truth_decode_sym = mapper.qam64(ori_fft)
        chan_decode_sym = mapper.qam64(clean_fft)
        pert_decode_sym = mapper.qam64(pert_fft)
    
    gt_bits, chan_bits, pert_bits = int_array_to_bit_array(ground_truth_decode_sym, \
                                                           chan_decode_sym, \
                                                           pert_decode_sym, \
                                                           num_bit=num_bit)

    num_bits, num_corr_bits_chan = compare_bits(gt_bits, chan_bits)
    num_bits, num_corr_bits_pert = compare_bits(gt_bits, pert_bits)

    # print(f"{num_bits = }, {num_corr_bits_chan = }, {num_corr_bits_pert}")

    return num_bits, num_corr_bits_chan, num_corr_bits_pert

# ---------------------------------------------------------------------
def main():
    ori_data_collection = get_ori_data()
    pert_data_collection = get_pert_data()
    clean_data_collection, data_label = get_clean_data()

    ttl_bit, ttl_chan_bit, ttl_pert_bit = 0, 0, 0

    for pkt_i, label in enumerate(data_label):
        if pkt_i%100 == 0:
            print(f"[{pkt_i}/{data_label.shape[0]}]")

        ori_data = ori_data_collection[pkt_i, 0, :] + 1.0j*ori_data_collection[pkt_i, 1, :]
        pert_data = pert_data_collection[pkt_i, 0, :] + 1.0j*pert_data_collection[pkt_i, 1, :]
        clean_data = clean_data_collection[pkt_i, 0, :] + 1.0j*clean_data_collection[pkt_i, 1, :]
        num_bit, num_bit_chan, num_bit_pert = calculate_ber(ori_data, clean_data, pert_data, label)
        ttl_bit += num_bit
        ttl_chan_bit += num_bit_chan
        ttl_pert_bit += num_bit_pert

    print(f"{ttl_chan_bit/ttl_bit}, {ttl_pert_bit/ttl_bit}")
    pass

# ---------------------------------------------------------------------
if __name__ == '__main__':
    main()