import numpy as np
import os, sys
import _pickle as pickle
import re
import matplotlib.pyplot as plt
from scipy.io import savemat
from scipy.io import loadmat

if os.system("clear") != 0:
    os.system("cls")


mod_list = ["WIFI-BPSK.mat", "WIFI-QPSK.mat", "WIFI-16QAM.mat", "WIFI-64QAM.mat", "BT-GFSK.dat", "BT-GFSK-LE1M.dat", "BT-GFSK-LE2M.dat", "BT-GFSK-S2Coding.dat", "BT-GFSK-S8Coding.dat", "ZIGBEE-OQPSK.dat"]
mod_idx = [x for x in range(len(mod_list))]

def main():
    with open('WirelessProtocol_325_1m.pkl', 'rb') as f:
        all_data = pickle.load(f, encoding='latin1')
    print(all_data.keys())

    for key in all_data.keys():
        print(all_data[key]['X'].shape)
        print(all_data[key]['Y'].shape)

    if True:
        return

    X = None
    Y = None
    dataset_dict = {}
    for (mod_name, mod_i) in zip(mod_list, mod_idx):
        mod_list_seq = mod_name.split('.')
        if mod_list_seq[1] == 'mat':
            # .mat file
            data_dict = loadmat(mod_name)
            _X = data_dict["data"]

            if _X.shape[0] > 20_000:
                _X = _X[0:20_000, :, :]
            
        else:
            # .dat file
            record_data = np.fromfile(open(mod_name), dtype=np.complex64)
            _X_c = record_data.reshape((20_000, 128))
            _X_i = np.expand_dims(np.real(_X_c), axis=1)
            _X_q = np.expand_dims(np.imag(_X_c), axis=1)

            _X = np.concatenate((_X_i, _X_q), axis=1)

        _Y = _Y = np.array([mod_i for x in range(_X.shape[0])])
        print(mod_list_seq[0], type(_X), _X.shape, _X.dtype, _Y.shape)

        dataset_dict[mod_list_seq[0]] = {
            "X": _X,
            "Y": _Y
            }

    print(dataset_dict.keys())
    if True:
        return
    save_filename = "WirelessProtocol_325_1m.pkl"
    with open(save_filename, 'wb') as f:
        pickle.dump(dataset_dict, f)
    pass

if __name__ == '__main__':
    main()