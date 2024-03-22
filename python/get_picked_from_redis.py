import redis
import _pickle as pickle
import sys, os
import numpy as np


ret = os.system("clear")
if ret != 0:
    os.system("cls")

def save_to_file(db, patch_name):
    try:
        key_pattern = f"SYSTEM:COLLECT:WIFI:*:{patch_name}:*"
        dataset = None
        for key in db.scan_iter(key_pattern):
            value = pickle.loads(db.get(key))
            real_part = np.expand_dims(np.real(value), axis=0)
            imag_part = np.expand_dims(np.imag(value), axis=0)

            two_ch_value = np.concatenate((real_part, imag_part), axis=0).reshape(1, 2, real_part.shape[1])
            if dataset is None:
                dataset = two_ch_value
            else:
                dataset = np.append(dataset, two_ch_value, axis=0)

        save_filename = "test.pkl"
        dataset_dict = {
            ('BPSK', 0): dataset
        }
        with open(save_filename, 'wb') as f:
            pickle.dump(dataset_dict, f)


    except Exception as exp:
        e_type, e_obj, e_tb = sys.exc_info()
        print(f'Exception occurs: {exp}. At line {e_tb.tb_lineno}')

def load_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f, encoding='latin1')

    print(f"{type(data) = }")
    keys = data.keys()
    for key in keys:
        print(f"{key = }")


def main():

    db = redis.StrictRedis(host="localhost", port=6379, db=0)
    unpacked_obj = pickle.loads(db.get("TEST_KEY"))
    print(f"{unpacked_obj = }, {unpacked_obj.shape}")


    key_list = db.keys("WIRELESS_PACKET:WIFI:*")
    for key in key_list:
        print(f"{key = }")
        unpacked_obj = pickle.loads(db.get(key))
        print(f"{unpacked_obj = }")
        print("\n****************\n")


    print(f"{type(db.keys('SYSTEM:COLLECT:WIFI:*'))}")
    print(f"{type(db.scan_iter('SYSTEM:COLLECT:WIFI:*'))}")
    patch_name = "2024_03_21_16_09_45"
    save_to_file(db, patch_name)
    load_pickle('test.pkl')

    pass

if __name__ == "__main__":
    main()
