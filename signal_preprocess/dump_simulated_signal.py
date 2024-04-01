import numpy as np
import redis as redis
import json
import sys, os
import _pickle as pickle
from scipy.io import savemat

ret = os.system('clear')
if ret != 0:
    os.system('cls')

# ----------------------------------------------
def save_as_pkl(filename, data_dict):
    with open(f"./{filename}.pkl", 'wb') as f:
        pickle.dump(data_dict, f)
    pass

def save_as_mat(filename):
    with open(f"./{filename}.pkl", 'rb') as f:
        data = pickle.load(f, encoding='latin1')

    dataset_values = list(data.values())[0]
    print(f"{dataset_values.shape = }")
    data_mat_dict = {
        "data": dataset_values
    }
    savemat(f"./{filename}.mat", data_mat_dict)
    pass

# ----------------------------------------------
def main():
    db = redis.Redis(host='localhost', port=6379, db=0)

    for encoding in range(8):
        print(f"{encoding = }")
        key = f"SYSTEM:SIMULATED:WIFI:{encoding}:48"

        value = pickle.loads(db.get(key))
        r_part = np.expand_dims(np.real(value), axis=0)
        i_part = np.expand_dims(np.imag(value), axis=0)

        two_ch_value = np.concatenate((r_part, i_part), axis=0).reshape(1, 2, r_part.shape[1])
        dataset_dict = {
            (encoding): two_ch_value
        }

        filename = f"Simulated_signal_{encoding}_48"
        save_as_pkl(filename, dataset_dict)
        save_as_mat(filename)

    pass

if __name__ == '__main__':
    main()
