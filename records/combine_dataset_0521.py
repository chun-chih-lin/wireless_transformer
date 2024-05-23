import numpy as np
import os, sys
import _pickle as pickle
import itertools

if os.system("clear") != 0:
    os.system("cls")

MOD_LIST = ["BPSK", "QPSK", "8PSK", "QAM16", \
            "QAM64", "AM-DSB", "AM-SSB", "PAM4", \
            "CPFSK", "GFSK", "WBFM", "WIFI-BPSK", \
            "WIFI-QPSK", "WIFI-16QAM", "WIFI-64QAM", "ZIGBEE-OQPSK", \
            "BT-GFSK-LE1M", "BT-GFSK-LE2M", "BT-GFSK-S2Coding", \
            "BT-GFSK-S8Coding", "RAND"]
MOD_IDS = [x for x in range(len(MOD_LIST))]


NON_PROCESS_MOD_LIST = ["BPSK", "QPSK", "8PSK", "QAM16", \
                        "QAM64", "AM-DSB", "AM-SSB", "PAM4", \
                        "CPFSK", "GFSK", "WBFM"]


MOD_LIST_1 = ["BPSK", "QPSK", "8PSK", "QAM16", \
            "QAM64", "AM-DSB", "AM-SSB", "PAM4", \
            "CPFSK", "GFSK", "WBFM"]
MOD_LIST_2 = ["WIFI-BPSK", "WIFI-QPSK", "WIFI-16QAM", \
            "WIFI-64QAM", "ZIGBEE-OQPSK", "BT-GFSK-LE1M", \
            "BT-GFSK-LE2M", "BT-GFSK-S2Coding", "BT-GFSK-S8Coding", "RAND"]


TP = [5, 0, -5, -10]
DIS = [5, 10, 15]
SR = 20
INTER = 0
CF = 2360

NN_PROCESS_PREFIX = ["Dataset_EIB_3F_Hallway_0521", "Dataset_EIB_room328_to_Hallway_0521"]

PREFIX = ["Dataset_EIB_3F_Hallway", "Dataset_EIB_room328_to_Hallway"]
PREFIX_1 = ["Dataset_EIB_3F_Hallway_0521", "Dataset_EIB_room328_to_Hallway_0521"]
PREFIX_2 = ["Dataset_EIB_3F_Hallway_0430", "Dataset_EIB_room328_to_Hallway"]

PKT_SIZE = 128
PKT_NUM = 20_000

def get_filename(comb):
    return f"Non_process_{comb[0]}_{comb[1]}_TP{comb[2]}_D{comb[3]}_SR20_CF2360_I0.dat"

def get_save_filename(comb):
    return f"{comb[0]}_{comb[1]}_TP{comb[2]}_D{comb[3]}_SR20_CF2360_I0.dat"

def process_packets():
    folder =  "./Dataset_0521/"
    combinations = itertools.product(NN_PROCESS_PREFIX, NON_PROCESS_MOD_LIST, TP, DIS)
    for comb in combinations:
        print('-----'*20)
        filename = get_filename(comb)
        save_filename = get_save_filename(comb)
        full_filename = os.path.join(folder, comb[0], filename)
        full_save_filename = os.path.join(folder, comb[0], save_filename)
        if os.path.exists(full_filename):
            if os.path.exists(full_save_filename):
                print(f"{full_save_filename} already exists. Skip")
                continue
            data = np.fromfile(open(full_filename), dtype=np.complex64)

            if data.shape[0] < PKT_NUM*PKT_SIZE:
                data = np.concatenate((data, data))
                data = data[:PKT_NUM*PKT_SIZE]
            num_pkt = int(data.shape[0]/PKT_SIZE)
            save_np = data.reshape((num_pkt, PKT_SIZE))

            save_np.tofile(full_save_filename)
            print(f"Saved to {full_save_filename}")
        else:
            print(f"{full_filename} does not exist.")
    pass

def combine_mods():
    save_folder = "./Dataset_21mod_0521/"
    root_folder_1 = "./Dataset_0521/"
    root_folder_2 = "./New_dataset_May/"
    for (prefix_1, prefix_2) in zip(PREFIX_1, PREFIX_2):
        print('-'*80)
        print(f"{prefix_1}, {prefix_2}")
        combinations = itertools.product(TP, DIS)
        combinations_1 = itertools.product(MOD_LIST_1, TP, DIS)
        combinations_2 = itertools.product(MOD_LIST_2, TP, DIS)

        filename_list = []

        for comb in combinations:
            print(f"TX: {comb[0]}, Dis: {comb[1]}")
            for mod in MOD_LIST_1:
                filename = f"{prefix_1}_{mod}_TP{comb[0]}_D{comb[1]}_SR20_CF2360_I0.dat"
                full_filename = os.path.join(root_folder_1, prefix_1, filename)
                if os.path.exists(full_filename):
                    filename_list.append(full_filename)
                    pass
                else:
                    print(f"{full_filename} does not exist")

            for mod in MOD_LIST_2:
                filename = f"{prefix_2}_{mod}_TP{comb[0]}_D{comb[1]}_SR20_CF2360_I0.dat"
                full_filename = os.path.join(root_folder_2, prefix_2, filename)
                if os.path.exists(full_filename):
                    filename_list.append(full_filename)
                    pass
                else:
                    print(f"{full_filename} does not exist")

            pkl_dict = {}
            X, Y = None, None
            for (filename, mod, mod_i) in zip(filename_list, MOD_LIST, MOD_IDS):
                record_data = np.fromfile(open(filename), dtype=np.complex64)
                print(f"{filename}, {mod}")
                if record_data.shape[0] > PKT_NUM*PKT_SIZE:
                    record_data = record_data[:PKT_NUM*PKT_SIZE]

                print(f"{record_data.shape = }")


                _X_c = record_data.reshape((PKT_NUM, PKT_SIZE))
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

            save_pkl_name = f"{prefix_1}-TP{comb[0]}_D{comb[1]}_SR20_CF2360_I0.pkl"
            save_filename = os.path.join(save_folder, save_pkl_name)
            print(f"Save to {save_filename}")

            if os.path.exists(save_filename):
                print(f"{save_filename} exist. Skip")
            else:
                with open(save_filename, 'wb') as f:
                    pickle.dump(dataset_dict, f)
    pass


def main():

    # "./Dataset_0521/"
    # "./New_dataset_May/"
    # process_packets()

    combine_mods()


    pass

if __name__ == '__main__':
    main()