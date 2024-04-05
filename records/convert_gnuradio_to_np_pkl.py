import numpy as np
import os, sys
import _pickle as pickle
import re
import matplotlib.pyplot as plt
from scipy.io import savemat

if os.system("clear") != 0:
    os.system("cls")


import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-p', help='Parsing file Prefix. e.g., room_325_1m.')
parser.add_argument('-s', help='source torch experience file directory.')
parser.add_argument('-t', help='target npy file directory.')
args = parser.parse_args()



def save_data_in_npy(src, tgt, filename):
    print(f"Saving {filename} from folder: {src} to {tgt}")
    mod = filename.split(".")[-1]
    save_filename_npy = filename + ".npy"
    save_filename_pkl = filename + ".pkl"
    save_filename_mat = filename + ".mat"

    src_filename = f"{src}{filename}"

    if os.path.isfile(src_filename):
        print("Already Exist")
        return

    record_data = np.fromfile(open(src_filename), dtype=np.complex64)

    dataset_dict = {
            "data": record_data
    }
    with open(save_filename_pkl, "wb") as f:
        pickle.dump(dataset_dict, f)
        pass

    savemat(save_filename_mat, dataset_dict)


def get_filenames_under_folder(src, prefix):
    mods = ["am_dsb", "am_ssb", "cpfsk", "fsk", "pam", "wbfm"]
    if os.path.isdir(src):
        dir_list = os.listdir(src)
        pattern = f"{prefix}.*"
        filename_list = [f"{prefix}.{fn}" for fn in mods]

        return filename_list
    else:
        return False

def main(args):
    file_list = get_filenames_under_folder(args.s, args.p)
    if file_list is False:
        print(f"Path: {args.s} is not a folder. Abort")
        exit()

    for filename in file_list:
        save_data_in_npy(args.s, args.t, filename)

if __name__ == "__main__":
    if args.s is None:
        print("Need source directory")
        exit()

    if args.p is None:
        print("Need parsing Prefix of files.")
        exit()

    if args.t is None:
        args.t = args.s
    main(args)
