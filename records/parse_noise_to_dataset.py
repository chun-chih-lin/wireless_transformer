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
CF = 2360

PKT_SIZE = 128
PKT_NUM = 20_000

SAVE_TP = [x for x in range(-10, 10, 5)]
print(f"{SAVE_TP = }")

def get_filename(prefix, comb):
    return f"Non_process_{prefix}_RAND_TP{TP}_D{comb[0]}_SR{comb[1]}_CF{CF}_I{comb[2]}.dat"

def get_save_filename(prefix, tp, comb):
    return f"{prefix}_RAND_TP{tp}_D{comb[0]}_SR{comb[1]}_CF{CF}_I{comb[2]}.dat"

def get_noise_files_from_source():

    print(f"{args.s = }")
    prefix = args.s.split("/")[1]
    # prefix = args.s.split("\\")[2]
    print(f"{prefix = }")

    combinations = itertools.product(DIS, SR, INTER)

    for comb in combinations:
        filename = get_filename(prefix, comb)
        full_filename = f"{args.s}{filename}"

        print("-"*50)
        print(f"Checking {full_filename}...")
        if os.path.exists(full_filename):
            print("Success")
            
            data = np.fromfile(open(full_filename), dtype=np.complex64)

            if data.shape[0] < PKT_NUM*PKT_SIZE:
                data = np.concatenate((data, data))
                data = data[:PKT_NUM*PKT_SIZE]

            print(f"{data.shape = }")
            num_pkt = int(data.shape[0]/PKT_SIZE)
            save_np = data.reshape((num_pkt, PKT_SIZE))
            print(f"{save_np.shape =}")
            for tp in SAVE_TP:
                save_filename = get_save_filename(prefix, tp, comb)
                full_save_filename = f"{args.s}{save_filename}"
                save_np.tofile(full_save_filename)
                print(f"Saved to {full_save_filename}")
            pass
        else:
            print("Failed!!!")
            print(f"{full_filename} is not exist.")
    pass

def main():

    if not os.path.isdir(args.s):
        print(f"{args.s} is not a directory.\nAbort.")
        exit()

    noise_files = get_noise_files_from_source()


if __name__ == "__main__":
    main()
