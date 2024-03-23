import _pickle as pickle
import numpy as np
import sys, os, json
import matplotlib.pyplot as plt

ret = os.system("clear")
if ret != 0:
    os.system("cls")

def load_pickle(full_path):
    if os.path.exists(full_path):
        print(f"Loading {full_path}")
        with open(full_path, 'rb') as f:
            data = pickle.load(f, encoding='latin1')
        return data
    return None

def get_signal_amp(signal):
    return signal[0, :]**2 + signal[1, :]**2

def visualization(signal):
    x_samples = [i for i in range(signal.shape[0])]
    plt.plot(x_samples, signal)
    plt.show()

def checking_through_dataset(dataset_folder, patch_info):
    keys = patch_info.keys()
    for key in keys:
        filename = patch_info[key]["Filename"]
        print(f"{filename = }")
        dataset = load_pickle(f"{dataset_folder}{filename}")
        if dataset is not None:
            dataset_values = list(dataset.values())[0]
            print(f"{dataset_values.shape = }")
            for sig_i in range(dataset_values.shape[0]):
                signal = dataset_values[sig_i, :, :].squeeze()
                print(f"{signal.shape = }")
                signal_amp = get_signal_amp(signal)
                print(f"{signal_amp.shape = }, {np.average(signal_amp)}")
                # visualization(signal_amp)
                

                if sig_i > 10:
                    break
            pass
        else:
            print(f"Dataset file: {filename} does not exist.")
        break
    pass

# ------------------------------------------------------

def show_example():
    print("Example: python check_dataset.py ./folder_to_check")
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
                    checking_through_dataset(dataset_folder, patch_info)
                    pass
            else:
                print("Input argument is not a folder.")
                show_example()
        else:
            print("Missing checking folder.")
            show_example()
        
    except Exception as exp:
        e_type, e_obj, e_tb = sys.exc_info()
        print(f'Exception: {exp}. At line {e_tb.tb_lineno}')

if __name__ == '__main__':
    main()