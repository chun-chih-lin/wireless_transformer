import numpy as np
import os, sys
import _pickle as pickle

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.')
parser.add_argument('-t', help='target npy file directory.')
parser.add_argument('-p', help='dataset pattern')
args = parser.parse_args()

if os.system("clear") != 0:
    os.system("cls")

# =====================================================
mod_list = ["BPSK", "QPSK", "8PSK", "QAM16", "QAM64", "AM-DSB", "AM-SSB", "PAM4", "CPFSK", "GFSK", "WBFM", "RAND"]
mod_idx = [x for x in range(len(mod_list))]

def get_filenames_under_folder(src, ptn):
    filename_list = []
    for mod in mod_list:
        filename = f"{mod}{ptn}dat"
        full_filename = f"{src}{filename}"
        if os.path.isfile(full_filename):
            filename_list.append(filename)
    return filename_list

def convert_to_pkl(args, file_list):
    src = args.s
    tgt = args.t

    pkl_dict = {}

    X, Y = None, None
    len_per_sample = 128

    for filename in file_list:
        full_filename = f"{src}{filename}"
        record_data = np.fromfile(open(filename), dtype=np.complex64)
        mod_name = filename.split('.')[0]
        mod_i = mod_list.index(mod_name)
        print(f"{full_filename = }, {filename = }, {mod_name = }, {mod_i = }")

        _X_c = record_data.reshape((20_000, 128))
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
        


# =====================================================
def main(args):
    print(sys.argv)
    file_list = get_filenames_under_folder(args.s, args.p)
    print(f"{file_list = }")
    if len(file_list) == 0:
        print(f"Path: {args.s} is not a folder. Abort")
        exit()

    for filename in file_list:
        print(filename)

    input_cmd = input("Is it right? [Y/n]")
    print(input_cmd)
    if input_cmd.upper() != "Y":
        print('Abort.')
        exit()

    #save_filename = None
    convert_to_pkl(args, file_list)

    # save_to_pkl_file(args, pkl_dict, save_filename)
    pass


if __name__ == '__main__':
    invalid_input = False
    if args.s is None:
        print("Need source directory")
        invalid_input = True

    if args.p is None:
        print("Need pattern")
        invalid_input = True


    if invalid_input:
        exit()

    if args.t is None:
        args.t = args.s
    main(args)
