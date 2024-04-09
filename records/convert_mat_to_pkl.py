import numpy as np
import os, sys
import _pickle as pickle
import re
import matplotlib.pyplot as plt
from scipy.io import savemat
from scipy.io import loadmat

if os.system("clear") != 0:
    os.system("cls")

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.')
parser.add_argument('-t', help='target npy file directory.')
args = parser.parse_args()

# -------------------------------------------------------------
def save_to_pkl_file(args, pkl_dict, file_pkl_name):
    mod_list = ["BPSK.0", "BPSK.1", "QPSK.2", "QPSK.3", "16QAM.4", "16QAM.5", "64QAM.6", "64QAM.7", "am_dsb", "am_ssb", "cpfsk", "fsk", "pam", "wbfm"]
    keys = pkl_dict.keys()

    mod_method_is_complete = True

    if mod_method_is_complete:
        full_filename = f"{args.t}{file_pkl_name}"
        print(f"Save to {full_filename}")
        # with open(full_filename, 'wb') as f:
        #     pickle.dump(pkl_dict, f)
    pass

def convert_to_pkl(args, filename):
    src = args.s
    tgt = args.t
    filepath = f"{src}{filename}"
    print(" ")
    pkl_dict = {}

    if not os.path.isfile(filepath):
        print(f"{filepath} is not a file.")
    else:
        filename_seg = filename.split(".")

        filename_prefix = filename_seg[0]
        filename_mod = ".".join(filename_seg[1:len(filename_seg)-2])
        save_pkl_name = f"{filename_prefix}.{filename_mod}.pkl"
        
        data_dict = loadmat(filepath)

        if 'data' in data_dict.keys():
            data = data_dict["data"]
        elif 'legitimate_packet' in data_dict.keys():
            data = data_dict["legitimate_packet"]
        else:
            return False
        num_packet = data.shape[0]
        len_data = data.shape[1]

        pkl_i = np.expand_dims(data.real, axis=1)
        pkl_q = np.expand_dims(data.imag, axis=1)

        pkl_c = np.concatenate((pkl_i, pkl_q), axis=1)

        pkl_dict[filename_mod] = pkl_c
        print(f"{save_pkl_name}, {pkl_c.shape = }")

        save_to_pkl_file(args, pkl_dict, save_pkl_name)
        # return filename_prefix
    pass

def get_filenames_under_folder(src):
    if os.path.isdir(src):
        filename_list = []
        dir_list = os.listdir(src)
        for filename in dir_list:
            file_seq = filename.split(".")
            if file_seq[-1] == "mat":
                filename_list.append(filename)

        return filename_list
    else:
        return False

# -------------------------------------------------------------
def main(args):
    file_list = get_filenames_under_folder(args.s)
    if file_list is False:
        print(f"Path: {args.s} is not a folder. Abort")
        exit()

    save_filename = None
    for filename in file_list:
        convert_to_pkl(args, filename)

    # save_to_pkl_file(args, pkl_dict, save_filename)
    pass

if __name__ == '__main__':
    if args.s is None:
        print("Need source directory")
        exit()
    if args.t is None:
        args.t = args.s
    main(args)