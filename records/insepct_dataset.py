import numpy as np
import os, sys
import _pickle as pickle

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.', required=True)
args = parser.parse_args()

if os.system("clear") != 0:
    os.system("cls")

def load_pickle_from_file():
    with open(args.s, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data

def main():
    data = load_pickle_from_file()

    for key in data.keys():
        print(f"{key}: dim = {data[key].shape}")

    pass

if __name__ == '__main__':
    main()