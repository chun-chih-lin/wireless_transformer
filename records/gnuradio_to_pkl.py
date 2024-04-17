import numpy as np
import os, sys
import _pickle as pickle

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.')
parser.add_argument('-t', help='target npy file directory.')
parser.add_argument('-p', help='dataset pattern')
parser.add_argument('-m', help='wireless signal type. [s/p]', default='s')
parser.add_argument('-y', help='yes to all', default=True, action='store_true')
args = parser.parse_args()

if os.system("clear") != 0:
    os.system("cls")

# =====================================================
def get_mod_list(t):
    if t == "simple":
        dataset_type = "simple"
        mod_list = ["BPSK", "QPSK", "8PSK", "QAM16", "QAM64", "AM-DSB", "AM-SSB", "PAM4", "CPFSK", "GFSK", "WBFM", "RAND"]
        # mod_idx = [x for x in range(len(mod_list))]
    else:
        # "protocol""
        dataset_type = "protocol"
        mod_list = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "BT-GFSK-S2Coding"]
        # mod_idx = [x for x in range(len(mod_list))]
    return mod_list, dataset_type


def get_filenames_under_folder(src, ptn, mod_list):
    filename_list = []
    for mod in mod_list:
        filename = f"{mod}{ptn}dat"
        full_filename = f"{src}{filename}"
        if os.path.isfile(full_filename):
            filename_list.append(filename)
        else:
            print(f"{filename} is not a file.")
    return filename_list

def convert_to_pkl(args, file_list, mod_list, dataset_type):
    src = args.s
    tgt = args.t
    ptn = args.p

    pkl_dict = {}

    X, Y = None, None
    len_per_sample = 128

    for filename in file_list:
        full_filename = f"{src}{filename}"
        record_data = np.fromfile(open(full_filename), dtype=np.complex64)

        if record_data.shape[0] > 20_000*128:
            record_data = record_data[:20_000*128]

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

    save_prefix = src.split('/')[1]
    ptn_seg = ptn.split('.')
    pattern = ".".join(ptn_seg)
    print(f"{ptn_seg = }, {pattern = }")

    save_pkl_name = f"{save_prefix}-{dataset_type}{pattern}pkl"
    save_filename = f"{tgt}{save_pkl_name}"

    if os.path.exists(save_filename):
        ow = input(f"Save file {save_filename} exists. Overwrite it? [y/N]")
        if ow.upper() == "N" or ow == "":
            print("Abort.")
            exit()

    confirm_cmd = input(f"Check and confirm to save to file: {save_filename} [Y/n]")
    if confirm_cmd.upper() == 'Y' or confirm_cmd == "":
        with open(save_filename, 'wb') as f:
            pickle.dump(dataset_dict, f)
        pass
    else:
        print("Abort saving.")
        
# =====================================================
def main(args):
    print(sys.argv)

    mod_list, dataset_type = get_mod_list(args.m)

    file_list = get_filenames_under_folder(args.s, args.p, mod_list)
    print(f"{file_list = }")
    if len(file_list) == 0:
        print(f"Path: {args.s} is not a folder. Abort")
        exit()

    for filename in file_list:
        print(filename)

    input_cmd = input("Is it right? [Y/n]")
    print(input_cmd, type(input_cmd))
    if input_cmd.upper() != "Y" and input_cmd != "":
        print('Abort.')
        exit()

    #save_filename = None
    convert_to_pkl(args, file_list, mod_list, dataset_type)

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

    if args.m == "s":
        args.m = "simple"
    elif args.m == "p":
        args.m = "protocol"
    else:
        print("Invalid modulation type. [s/w]")
        invalid_input = True

    if invalid_input:
        exit()

    print(f"{args.y = }")
    if args.y is None:
        args.y = False
    print(f"{args.y = }")

    if args.t is None:
        args.t = args.s
    main(args)
