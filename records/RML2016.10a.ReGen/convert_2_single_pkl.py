import numpy as np
import redis as redis
import json
import sys, os
import _pickle as pickle

ret = os.system('clear')
if ret != 0:
    os.system('cls')


def main():
    mod_list = ["BPSK", "QPSK", "8PSK", "QAM16", "QAM64", "AM-DSB", "AM-SSB", "PAM4", "CPFSK", "GFSK", "WBFM"]
    mod_idx = [x for x in range(len(mod_list))]
    print(mod_idx)

    len_per_sample = 128

    X = None
    Y = None

    for mod, mod_i in zip(mod_list, mod_idx):
        print(f"{mod = }, {mod_i = }")
        src_filename = f"{mod}.dat"
        record_data = np.fromfile(open(src_filename), dtype=np.complex64)


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
            "X": X,
            "Y": Y
            }

    print(dataset_dict['X'].shape)
    print(dataset_dict['Y'].shape)
    if True:
        return

    save_filename = "RML2016.10a.ReGeneratedWireless.pkl"
    with open(save_filename, 'wb') as f:
        pickle.dump(dataset_dict, f)

    pass

if __name__ == "__main__":
    main()
