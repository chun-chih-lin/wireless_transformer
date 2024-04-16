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

def get_filenames_under_folder(src, ptn):
    if os.path.isdir(src):
        filename_list = []
        dir_list = os.listdir(src)
        for filename in dir_list:
            file_seq = filename.split(".")
            
            if file_seq[-1] == "dat" and filename.find(ptn) >= 0:
                filename_list.append(filename)
        
        return filename_list
    else:
        return False


def convert_to_pkl(args, filename):
    mod_list = ["BPSK", "QPSK", "8PSK", "QAM16", "QAM64", "AM-DSB", "AM-SSB", "PAM4", "CPFSK", "GFSK", "WBFM", "RAND"]

    src = args.s
    tgt = args.t
    filepath = f"{src}{filename}"
    print(" ")
    pkl_dict = {}

    X, Y = None, None
    len_per_sample = 128

    if not os.path.isfile(filepath):
        print(f"{filepath} is not a file.")
    else:
        print(filepath)
        record_data = np.fromfile(open(filepath), dtype=np.complex64)


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
    if file_list is False:
        print(f"Path: {args.s} is not a folder. Abort")
        exit()

    for filename in file_list:
        print(filename)

    input_cmd = input("Is it right? [Y/n]")
    print(input_cmd)
    if input_cmd.upper() != "Y":
        print('Abort.')

    
    #save_filename = None
    for filename in file_list:
        convert_to_pkl(args, filename)

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
