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


def load_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data


def check_file(filenames):
    for filename in filenames:
        print("\n"*2)
        print("="*50)
        print(f"{filename = }")
        full_dir = f"{args.s}{filename}"
        data = load_pickle(full_dir)

        if data['X'].shape[0] != 200_000:
            print(f"{filename} has dimension only: {data['X'].shape}. Skip.")
            continue
        print("Before trimming:")
        print(f"  {data['X'].shape = }")

        S2 = data['X'][20_000*7, :, :]
        S8 = data['X'][20_000*8, :, :]

        x_delete_idx = [x for x in range(20_000*8, 20_000*9)]
        y_delete_idx = [x for x in range(20_000*9, 20_000*10)]
        if np.array_equal(S2, S8):
            data['X'] = np.delete(data['X'], x_delete_idx, axis=0)
            data['Y'] = np.delete(data['Y'], y_delete_idx, axis=0)

            print("After trimming:")
            print(f"  {data['X'].shape = }")
            print(f"  {data['Y'].shape = }")
            print(np.min(data['Y']), np.max(data['Y']))


            proceed = "Y"
            if not args.y:
                proceed = input("Proceed to save? [y/N]")
            if proceed.upper() != 'Y':
                print("Abort.")
                continue

            print(f"Save to file: {args.s}{filename}")

            with open(f"{args.s}{filename}", 'wb') as f:
                pickle.dump(data, f)
        else:
            print("It is a right file. Skip.")
    pass


def main():
    filenames = os.listdir(args.s)
    real_file_list = []
    for filename in filenames:
        if filename.find('.pkl') >= 0:
            real_file_list.append(filename)

    print(f"{real_file_list = }")

    check_file(real_file_list)
    pass

if __name__ == '__main__':
    main()