import numpy as np
import os, sys
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.')
parser.add_argument('-t', help='target npy file directory.')
parser.add_argument('-p', help='dataset pattern')
args = parser.parse_args()

if os.system('clear') != 0:
    os.system('cls')

pkt_len_list = {
    "BPSK": 1280,
    "QPSK": 880,
    "16QAM": 640,
    "64QAM": 560
}

def energy(ary):
    return ary * np.conj(ary)

def check_plot(data, e_data):
    plt.plot(data.real)
    plt.plot(data.imag)
    plt.plot(e_data)
    plt.show()
    pass

def is_long_enough(ary, pkt_s, pkt_energy_threshold=0.2):
    # e_ary = energy(ary)
    e_ary = np.abs(ary)
    e_ary_mean = np.mean(e_ary.real)
    # print(f"[{pkt_s}] {e_ary_mean = }, {pkt_energy_threshold = }")
    return e_ary_mean >= pkt_energy_threshold

    pass


def trim(data, pkt_len, mod):
    print(f"{data.shape = }")

    # e_threshold = 0.01
    # sec_threshold = 0.0008

    # --------------------------------
    # 50 db outdoor
    e_threshold = 0.0001
    e_threshold = 0.00006
    sec_threshold = 0.00038
    pkt_e_threshold_list = {
        "BPSK": 0.0025,
        "QPSK": 0.0020,
        "16QAM": 0.0015,
        "64QAM": 0.0015
    }

    pkt_energy_threshold = pkt_e_threshold_list[mod]

    e_data = energy(data)
    raw_e_data = e_data.copy()
    # check_plot(data, e_data)

    above_t_data = np.where(e_data >= e_threshold)[0]
    # plt.plot(data.real, alpha=.2)
    # plt.plot(data.imag, alpha=.2)
    # [plt.axvline(x, color='r') for x in above_t_data]
    # plt.show()

    ttl_pkt = None
    pkt_s_list = []

    print(f"{pkt_s_list = }")
    plt.plot(data.real, alpha=.2)
    plt.plot(data.imag, alpha=.2)
    # plt.plot(np.abs(data))
    plt.show()

    return ttl_pkt

def main(args):

    src = args.s
    ptn = args.p

    for mod in pkt_len_list.keys():
        dat_filename = f"{src}WIFI-{mod}{ptn}dat"
        print(f"{dat_filename = }")

        pkt_len = pkt_len_list[mod]

        s = None
        e = None

        s = 0
        e = 1_000_000

        if os.path.isfile(dat_filename):
            print("is file")
            data = np.fromfile(dat_filename, dtype=np.complex64)
            print(data.shape)

            if s is None or e is None:
                s = 0
                e = data.shape[0]

            plot_data = data[s:e]
            trimmed_pkt = trim(plot_data, pkt_len, mod)
            # print(f"{trimmed_pkt.shape = }")

            # save_dat_name = f"{src}Trimmed-WIFI-{mod}{ptn}dat"
            # print(f"{save_dat_name = }")
            # trimmed_pkt.tofile(save_dat_name)
        else:
            print("not a file")

        # if True:
        #     break

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

    main(args)

