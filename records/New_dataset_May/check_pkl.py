import numpy as np
import sys, os
import itertools
import _pickle as pickle
import gzip
import argparse

parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.', required=True)
parser.add_argument('-y', help='Yes to all', default=False, action='store_true')
args = parser.parse_args()

if os.system('clear') != 0:
    os.system('cls')



def main():
    with open(args.s, 'rb') as f:
        data = pickle.load(f, encoding='latin1')

    print(data['X'].shape)
    print(data['Y'].shape)


    show_list = [x*20_000 for x in range(10)]
    print(data['Y'][show_list])
    print(data['X'][show_list, :, :])


if __name__ == "__main__":
    main()

