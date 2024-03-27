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

def conver_folder(dataset_folder, patch_info):
    keys = patch_info.keys()
    for key in keys:
        filename = patch_info[key]["Filename"]
        mat_filename = f"{patch_info[key]['MOD']}.{patch_info[key]['MCS']}.{key}.mat"
        mat_full_filename = f"{dataset_folder}{mat_filename}"
        print("----")
        dataset = load_pickle(f"{dataset_folder}{filename}")

        if dataset is not None:
            dataset_values = list(dataset.values())[0]
            print(f"{dataset_values.shape = }")
            data_mat_dict = {
                "data": dataset_values
            }
            savemat(mat_full_filename, data_mat_dict)
            print(f"Save to {mat_full_filename}")


    pass

# ------------------------------------------------------

def show_example():
    print("Example: python pkl_to_mat.py ./folder_to_convert")
    pass

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
    try:
        if len(sys.argv) == 2:
            dataset_folder = sys.argv[1]
            if os.path.isdir(dataset_folder):
                patch_info = get_patch_info(dataset_folder)
                if patch_info is not None:
                    conver_folder(dataset_folder, patch_info)
                    pass
            else:
                print("Input argument is not a folder.")
                show_example()
        else:
            print("Missing folder.")
            show_example()
    except Exception as exp:
        e_type, e_obj, e_tb = sys.exc_info()
        print(f'Exception: {exp}. At line {e_tb.tb_lineno}')


if __name__ == '__main__':
    main()