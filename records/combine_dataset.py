"""
This is used for combining dataset for the same scenario into one file.
Example:
    python ./combine_dataset.py -s ./Dataset_modulation/ -p room_328
"""

import numpy as np
import os, sys
import _pickle as pickle

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.', required=True)
parser.add_argument('-t', help='target npy file directory.')
parser.add_argument('-p', help='dataset pattern', required=True)
parser.add_argument('-i', help='Insepect the first 1_000_000 samples', default=False, action='store_true')
args = parser.parse_args()

if os.system("clear") != 0:
    os.system("cls")

# ------------------------------------------------
PROTOCOL_LIST = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "BT-GFSK-S8Coding"]
SAMPLE_LEN = 20_000

def trim_for_wifi(ori_data):

    CON_IDX = {
        "WIFI-BPSK": {
            "s1": 320, 
            "s2": 640
        },
        "WIFI-QPSK": {
            "s1": 320, 
            "s2": 640
        },
        "WIFI-16QAM": {
            "s1": 320, 
            "s2": 512
        },
        "WIFI-64QAM": {
            "s1": 320, 
            "s2": 432
        }
    }

    X = None  # data input
    Y = None  # modulation label (e.g., BPSK)
    for mod in PROTOCOL_LIST:
        if mod in ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM"]:
            _X_1 = ori_data[mod]["X"][:, :, CON_IDX[mod]["s1"]:CON_IDX[mod]["s1"]+128]
            _X_2 = ori_data[mod]["X"][:, :, CON_IDX[mod]["s2"]:CON_IDX[mod]["s2"]+128]
            _X = np.concatenate((_X_1, _X_2))
            _X = _X[0:SAMPLE_LEN, :, :]

            _Y_1 = ori_data[mod]["Y"]
            _Y_2 = ori_data[mod]["Y"]

            _Y = np.concatenate((_Y_1, _Y_2))
            _Y = _Y[0:SAMPLE_LEN]
        else:
            _X = ori_data[mod]["X"]
            _Y = ori_data[mod]["Y"]

        if X is None:
            X = _X
            Y = _Y
        else:
            X = np.concatenate((X, _X))
            Y = np.concatenate((Y, _Y))

    data = {
        'X': X,
        'Y': Y
    }
    return data
    pass


# ------------------------------------------------
def load_pickle_from_file(filename):
    full_filename = f"{args.s}{filename}"
    with open(full_filename, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data

def combine(filename_list, filename_prefix):
    print("\n----")
    print("Combining...")
    dataset_idx = [i for i in range(len(filename_list))]
    filename_list.sort()
    for (filename, dataset_id) in zip(filename_list, dataset_idx):
        print(f"{filename = }, with {dataset_id = }")
    proceed = input("Check sorted data. Proceed? [Y/n]")
    if proceed.upper() not in ["", "Y"]:
        abort()

    X = None  # data input
    Y = None  # modulation label (e.g., BPSK)
    Z = None  # scenario label (e.g., snr)

    dataset_dict = {}
    for (filename, dataset_id) in zip(filename_list, dataset_idx):
        print(f"---")
        full_filename = f"{args.s}{filename}"
        data = load_pickle_from_file(filename)

        if filename.find("protocol") > 0:
            print("Trim for WIFI first")
            data = trim_for_wifi(data)

        _X = data["X"]
        _Y = data["Y"]
        _Z = np.full(_Y.shape, dataset_id)

        if X is None:
            X = _X
            Y = _Y
            Z = _Z
        else:
            X = np.concatenate((X, _X))
            Y = np.concatenate((Y, _Y))
            Z = np.concatenate((Z, _Z))

        print(X.shape, Y[0:5], Y.shape, Z[0:5], Z.shape)

    dataset_dict = {
        'X': X,
        'Y': Y,
        'Z': Z
    }

    save_filename = f"{args.s}{filename_prefix}.pkl"

    confirm_save = input(f"Confirm save to file: {save_filename}? [y/N]")
    if confirm_save.upper() == 'Y':
        with open(save_filename, 'wb') as f:
            pickle.dump(dataset_dict, f)

        print(f"Saved to {save_filename}")
    pass



# ------------------------------------------------
def abort():
    print('Abort.')
    exit()
    pass

def make_sure_only_single_type_dataset(filename_list):
    print("All find: ")
    filename_prefix = None
    for filename in filename_list:
        cur_prefix = filename.split('.')[0]
        print(f"{filename = }")
        if filename_prefix is None:
            filename_prefix = cur_prefix
        elif filename_prefix != cur_prefix:
            print("------")
            print("Mixed dataset.")
            print(f"\t{filename_prefix}")
            print(f"\t{cur_prefix}")
            abort()
    return filename_prefix

def gather_files_from_pattern():
    file_list = os.listdir(args.s)
    filename_list = []
    for filename in file_list:
        if filename.find(args.p) >= 0 and len(filename.split(".")) > 2:
            filename_list.append(filename)

    if len(filename_list) == 0:
        print("Found none.")
        abort()
    return filename_list

def is_already_exist(filename_prefix):
    save_filename = f"{args.s}{filename_prefix}.pkl"
    if os.path.exists(save_filename):
        proceed = input(f"File {save_filename} is already existed. Proceed? [y/N]")
        if proceed.upper() in ["", "N"]:
            abort()
    pass

def main():
    filename_list = gather_files_from_pattern()
    filename_prefix = make_sure_only_single_type_dataset(filename_list)
    is_already_exist(filename_prefix)

    proceed = input("Proceed combining? [Y/n]")
    if proceed.upper() == "Y" or proceed == "":
        combine(filename_list, filename_prefix)
    else:
        abort()
    pass

if __name__ == '__main__':
    main()