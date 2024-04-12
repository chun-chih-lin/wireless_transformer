import _pickle as pickle
import numpy as np
import os, sys, json
from scipy.io import savemat

ret = os.system("clear")
if ret != 0:
    os.system("cls")

# ------------------------------------------------------
def load_pickle(full_path):
    if os.path.exists(full_path):
        print(f"Loading {full_path}")
        with open(full_path, 'rb') as f:
            data = pickle.load(f, encoding='latin1')
        return data
    return None

def get_patch_info(folder_name):
    patch_file_name = f"{folder_name}patch_info.json"
    if os.path.exists(patch_file_name):
        with open(f"{folder_name}patch_info.json", 'r') as f:
            patch_info = json.load(f)
        return patch_info
    else:
        print("The input folder is not a dataset folder. Lack of path_info.json file.")
        return None

def main():
    mod_list = ["BPSK", "QPSK", "16QAM", "64QAM"]
    patch_info = get_patch_info("./")


    ttl_n = [0, 0, 0, 0, 0, 0, 0, 0]

    for key in patch_info.keys():
        print(key)
        filename = patch_info[key]["Filename"]
        mcs = patch_info[key]['MCS']
        mat_filename = f"{patch_info[key]['MOD']}.{patch_info[key]['MCS']}.{key}.mat"
        mat_full_filename = f"./wifi/{mat_filename}"

        print(filename, mat_full_filename)
        dataset = load_pickle(filename)
        if dataset is not None:
            dataset_values = list(dataset.values())[0]
            print(f"{dataset_values.shape = }")

            ttl_n[mcs] += dataset_values.shape[0]

            data_mat_dict = {
                "data": dataset_values
            }
            savemat(mat_full_filename, data_mat_dict)
    print(ttl_n)


if __name__ == '__main__':
    main()
