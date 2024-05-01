import numpy as np
import sys, os
import itertools
import _pickle as pickle

import argparse

parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.', required=True)
parser.add_argument('-y', help='Yes to all', default=False, action='store_true')
args = parser.parse_args()


def main():
    print("Main")
    pass

if __name__ == '__main__':
    main()