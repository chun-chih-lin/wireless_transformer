import numpy as np
import redis as redis
import json
import sys, os
import _pickle as pickle

import argparse
parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.')
parser.add_argument('-t', help='target npy file directory.')
parser.add_argument('-p', help='dataset pattern')
parser.add_argument('-i', help='Insepect the first 1_000_000 samples', default=False, action='store_true')
args = parser.parse_args()

ret = os.system('clear')
if ret != 0:
    os.system('cls')


def main():
    print(f"{args = }")
    pass

if __name__ == "__main__":
    invalid_input = False
    if args.s is None:
        print("Need source directory")
        invalid_input = True

    if args.p is None:
        print("Need pattern")
        invalid_input = True

    if invalid_input:
        exit()

    if args.t is None:
        args.t = args.s
    main()
