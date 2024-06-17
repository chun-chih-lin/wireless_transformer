import numpy as np
import _pickle as pickle
import sys, os

if os.system("clear") != 0:
    os.system("cls")

GRANT_SAVE_DATA_ROOT = "sub_dataset"

GET_DATA_ROOT = ["Dataset_21mod_0521", "Dataset_10mod_0524"]
SAVE_DATA_ROOT = ["Dataset_21mod", "Dataset_10mod"]

PREFIX_1 = ["Dataset_EIB_3F_Hallway_0521", "Dataset_EIB_room328_to_Hallway_0521"]
PREFIX_2 = ["Dataset_EIB_3F_Hallway_0430", "Dataset_EIB_room328_to_Hallway", "Dataset_EIB_Outdoor"]
SAVE_PREFIX = ["Indoor_LOS", "Indoor_NLOS", "Outdoor_LOS"]
PREFIX = {
    "0": PREFIX_1,
    "1": PREFIX_2
}


CONDITIONS = ["TP5_D5_SR20_CF2360_I0.pkl", "TP5_D10_SR20_CF2360_I0.pkl", "TP5_D15_SR20_CF2360_I0.pkl", \
              "TP0_D5_SR20_CF2360_I0.pkl", "TP0_D10_SR20_CF2360_I0.pkl", "TP0_D15_SR20_CF2360_I0.pkl", \
              "TP-5_D5_SR20_CF2360_I0.pkl", "TP-5_D10_SR20_CF2360_I0.pkl", "TP-5_D15_SR20_CF2360_I0.pkl", \
              "TP-10_D5_SR20_CF2360_I0.pkl", "TP-10_D10_SR20_CF2360_I0.pkl", "TP-10_D15_SR20_CF2360_I0.pkl", \
              ]

SAMPLE_PRE_MOD = 20_000
SAVE_SAMPLE_PRE_MOD = 1000

def load_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data

def main():
    for cond in CONDITIONS:
        for i, (root, save_root) in enumerate(zip(GET_DATA_ROOT, SAVE_DATA_ROOT)):
            prefixes = PREFIX[str(i)]
            for p_i, prefix in enumerate(prefixes):
                print("="*80)
                filename = f"{prefix}_{cond}"

                save_postfix_seg = cond.split("_")[0:2]
                save_postfix = "_".join(save_postfix_seg)

                full_filename = os.path.join(root, prefix, filename)
                if not os.path.exists(full_filename):
                    print(f"{full_filename} does not exist.")
                    break
                data = load_pickle(full_filename)
                n_cls = int(data['X'].shape[0]/SAMPLE_PRE_MOD)
                print(data['X'].shape)
                print(data['Y'].shape)
                print(f"{n_cls = }")

                X = None
                Y = None

                for n in range(n_cls):
                    offset = 0*SAMPLE_PRE_MOD
                    idc = [x + offset for x in range(SAVE_SAMPLE_PRE_MOD)]

                    _X = data['X'][idc, :, :]
                    _Y = data['Y'][idc]

                    if X is None:
                        X = _X
                        Y = _Y
                    else:
                        X = np.concatenate((X, _X), axis=0)
                        Y = np.concatenate((Y, _Y), axis=0)
                    print(f"{X.shape = }, {Y.shape = }")

                save_data = {
                    "X": X,
                    "Y": Y
                }

                save_filename = f"{SAVE_PREFIX[p_i]}_{save_postfix}.pkl"
                save_sub_dataset_fullname = os.path.join(GRANT_SAVE_DATA_ROOT, save_root, save_filename)

                if not os.path.exists(os.path.join(GRANT_SAVE_DATA_ROOT, save_root)):
                    os.mkdir(os.path.join(GRANT_SAVE_DATA_ROOT, save_root))

                print(f"Save to {save_sub_dataset_fullname}")

                with open(save_sub_dataset_fullname, 'wb') as f:
                    pickle.dump(save_data, f)
                # exit()



if __name__ == '__main__':
    main()