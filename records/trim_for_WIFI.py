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


def trim(data, pkt_len):
    print(f"{data.shape = }")

    e_threshold = 0.01
    sec_threshold = 0.0008

    e_data = energy(data)

    check_plot(data, e_data)

    above_t_data = np.where(e_data >= e_threshold)[0]
    under_t_data = np.where(e_data < e_threshold)[0]

    e_data[above_t_data] = 0.25
    e_data[under_t_data] = e_data[under_t_data] + 0.2*e_data[under_t_data-1]

    

    idx_data = np.where(e_data > sec_threshold)[0]

    # print(f"{idx_data = }")

    _idx_data = np.array([0 for x in range(idx_data.shape[0])])
    _idx_data[0:-1] = idx_data[1:] - idx_data[0:-1]
    _idx_data[-1] = 5
    # print(f"{_idx_data = }")

    pkt_e_idx_data = np.where(_idx_data > 1)[0]
    print(f"{pkt_e_idx_data.shape = }")

    ttl_pkt = None
    for idx in pkt_e_idx_data:
        pkt_s = idx_data[idx] - pkt_len
        # plt.axvline(idx_data[idx], color='k')
        # plt.axvline(pkt_s, color='r')
        # print(f"{pkt_s = }")
        if ttl_pkt is None:
            ttl_pkt = np.expand_dims(data[pkt_s:pkt_s+pkt_len], axis=0)
        else:
            ttl_pkt = np.concatenate((ttl_pkt, np.expand_dims(data[pkt_s:pkt_s+pkt_len], axis=0)))

        # plt.plot(data[pkt_s:pkt_s+pkt_len].real)
        # plt.plot(data[pkt_s:pkt_s+pkt_len].imag)
        # plt.show()

    # plt.show()
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
        e = 100_000

        if os.path.isfile(dat_filename):
            print("is file")
            data = np.fromfile(dat_filename, dtype=np.complex64)
            print(data.shape)

            if s is None or e is None:
                s = 0
                e = data.shape[0]

            plot_data = data[s:e]
            print(plot_data.shape)
            trimmed_pkt = trim(plot_data, pkt_len)

            print(f"{trimmed_pkt.shape = }")

            # mean_e = np.zeros((trimmed_pkt.shape[0], ))
            # for pkt_i in range(trimmed_pkt.shape[0]):
            #     mean_e[pkt_i] = np.mean(energy(trimmed_pkt[pkt_i, :]))

            # for i in range(trimmed_pkt.shape[0]):
            #     plt.plot(trimmed_pkt[i, :].real)
            #     plt.plot(trimmed_pkt[i, :].imag)

            # plt.plot(mean_e.real)
            # plt.plot(mean_e.imag)
            # plt.ylim((0, 0.1))
            # plt.show()

            dataset = {
                'data': trimmed_pkt
            }
            # savemat(f"WIFI-{sys.argv[1]}.mat", dataset)
        else:
            print("not a file")

        if True:
            break

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

