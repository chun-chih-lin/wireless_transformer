import numpy as np
import sys, os
import itertools
import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.', required=True)
parser.add_argument('-y', help='Yes to all', default=False, action='store_true')
args = parser.parse_args()


TP = -10
DIS = [5, 10, 15]
SR = [5, 20]
INTER = [0, 1]

def get_noise_files_from_source():

    combinations = itertools.product(DIS, SR, INTER)

    for comb in combinations:
        print(list(comb))

    pass

def main():

    if not os.path.isdir(args.s):
        print(f"{args.s} is not a directory.\nAbort.")
        exit()

    noise_files = get_noise_files_from_source()


if __name__ == "__main__":
    main()
