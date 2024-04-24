import numpy as np
import os, sys
import _pickle as pickle

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source folder.', required=True)
parser.add_argument('-n', help='source name.', required=True)
args = parser.parse_args()

if os.system("clear") != 0:
    os.system("cls")


def load_dat_from_file(full_filename):
    return np.fromfile(open(full_filename), dtype=np.complex64)

def load_pickle_from_file():
    with open(args.s, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data

def main():


    full_filename = f"{args.s}{args.n}"
    if not os.path.exists(full_filename):
        print(f"{full_filename} is not a file.")
        exit()
    
    data = load_dat_from_file(full_filename)
    

    pass

if __name__ == '__main__':
    main()