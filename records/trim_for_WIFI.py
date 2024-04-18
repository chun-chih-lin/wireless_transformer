import numpy as np
import os, sys
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', help='source torch experience file directory.')
parser.add_argument('-t', help='target npy file directory.')
parser.add_argument('-p', help='dataset pattern')
parser.add_argument('-i', help='Insepect the first 1_000_000 samples', default=False, action='store_true')
args = parser.parse_args()

if os.system('clear') != 0:
    os.system('cls')

pkt_len_list = {
    "BPSK": 1280,
    "QPSK": 880,
    "16QAM": 640,
    "64QAM": 560
}

# INSPECT_LEN = 1_000_000
INSPECT_LEN = 10_000

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
    print(f"[{pkt_s}] {e_ary_mean = }, {pkt_energy_threshold = }")
    return e_ary_mean >= pkt_energy_threshold

def trim(data, pkt_len, tx_pwr, mod):
    print(f"{data.shape = }")

    # e_threshold = 0.01
    # sec_threshold = 0.0008

    # --------------------------------
    # 50 db outdoor
    # e_threshold = 0.0001
    e_threshold = 0.0025
    sec_threshold = 0.00038
    pkt_e_threshold_list = {
        "5": {
            "BPSK": 0.0025,
            "QPSK": 0.0020,
            "16QAM": 0.0015,
            "64QAM": 0.0015
        },
        "0": {
            "BPSK": 0.0025,
            "QPSK": 0.0020,
            "16QAM": 0.0015,
            "64QAM": 0.0015
        },
        "-5": {
            "BPSK": 0.0025,
            "QPSK": 0.0020,
            "16QAM": 0.0015,
            "64QAM": 0.0015
        },
        "-10": {
            "BPSK": 0.0025,
            "QPSK": 0.0020,
            "16QAM": 0.0015,
            "64QAM": 0.0015
        },
        "-15": {
            "BPSK": 0.0025,
            "QPSK": 0.0020,
            "16QAM": 0.0015,
            "64QAM": 0.0015
        },
        "-20": {
            "BPSK": 0.0027,
            "QPSK": 0.0020,
            "16QAM": 0.0015,
            "64QAM": 0.0015
        }
    }

    pkt_energy_threshold = pkt_e_threshold_list[tx_pwr][mod]

    # e_data = energy(data)
    e_data = np.abs(data)
    raw_e_data = e_data.copy()
    # check_plot(data, e_data)

    above_t_data = np.where(e_data >= e_threshold)[0]
    # print(f"{above_t_data = }")
    # under_t_data = np.where(e_data < e_threshold)[0]

    # e_data[above_t_data] = 0.25
    # e_data[under_t_data] = e_data[under_t_data] + 0.2*e_data[under_t_data-1]

    # idx_data = np.where(e_data > sec_threshold)[0]

    # print(f"{idx_data = }")

    # _idx_data = np.array([0 for x in range(idx_data.shape[0])])
    # _idx_data[0:-1] = idx_data[1:] - idx_data[0:-1]
    # _idx_data[-1] = 5
    # # print(f"{_idx_data = }")

    # pkt_e_idx_data = np.where(_idx_data > 1)[0]
    # print(f"{pkt_e_idx_data.shape = }, {pkt_e_idx_data = }")


    # for s in above_t_data:
    #     e = is_long_enough(data[s:s+pkt_len], s, pkt_energy_threshold=pkt_energy_threshold)

    # plt.plot(data.real, alpha=.2)
    # plt.plot(data.imag, alpha=.2)
    # [plt.axvline(x, color='r') for x in above_t_data]
    # plt.show()

    ttl_pkt = None
    pkt_s_list = []

    print(f"{above_t_data = }")

    last_pkt_end = None
    for pkt_s in above_t_data:
        # print(f"{pkt_s = }")

        if last_pkt_end is not None and pkt_s <= last_pkt_end:
            continue

        detect_pkt = data[pkt_s:pkt_s+pkt_len]
        if is_long_enough(detect_pkt, pkt_s, pkt_energy_threshold=pkt_energy_threshold):
            last_pkt_end = pkt_s+pkt_len

            pkt_s_list.append(pkt_s)

            if ttl_pkt is None:
                ttl_pkt = np.expand_dims(data[pkt_s:pkt_s+pkt_len], axis=0)
            else:
                ttl_pkt = np.concatenate((ttl_pkt, np.expand_dims(data[pkt_s:pkt_s+pkt_len], axis=0)))
        else:
            print(f"{pkt_s} is not long enough.")

    if data.shape[0] <= INSPECT_LEN:
        print(f"{pkt_s_list = }")
        f, (ax1, ax2) = plt.subplots(2, 1)
        ax1.plot(data.real, alpha=.2)
        ax1.plot(data.imag, alpha=.2)
        # ax1.plot(e_data, color='y')
        ax1.plot(np.abs(data))
        [ax1.axvline(x, color='r') for x in pkt_s_list]
        ax1.axhline(e_threshold, color='r')

        if ttl_pkt is not None:
            for i in range(ttl_pkt.shape[0]):
                ax2.plot(ttl_pkt[i, :].real)
                ax2.plot(ttl_pkt[i, :].imag)
        plt.show()
    else:
        print(f"Data shape too large [{data.shape[0]} > {INSPECT_LEN}]. Skip plot.")

    return ttl_pkt

    # if True:
    #     return

    # for idx in pkt_e_idx_data:
    #     print(f"{idx = }")
    #     pkt_s = idx_data[idx] - pkt_len

    #     # plt.axvline(idx_data[idx], color='k')
    #     # plt.axvline(pkt_s, color='r')
    #     # plt.plot(data.real, alpha=.2)
    #     # plt.plot(data.imag, alpha=.2)
    #     # plt.plot(e_data)
    #     # print(f"{pkt_s = }")


    #     detect_pkt = data[pkt_s:pkt_s+pkt_len]
    #     if is_long_enough(detect_pkt, pkt_energy_threshold=pkt_energy_threshold):
    #         if ttl_pkt is None:
    #             ttl_pkt = np.expand_dims(data[pkt_s:pkt_s+pkt_len], axis=0)
    #         else:
    #             ttl_pkt = np.concatenate((ttl_pkt, np.expand_dims(data[pkt_s:pkt_s+pkt_len], axis=0)))

    #         plt.plot(data[pkt_s:pkt_s+pkt_len].real)
    #         plt.plot(data[pkt_s:pkt_s+pkt_len].imag)
    #         plt.show()
    #         # break

    # # plt.show()
    # return ttl_pkt

def main(args):

    src = args.s
    ptn = args.p

    tx_pwr = ptn.split('.')[1]
    print(f"{tx_pwr = }")

    for mod in pkt_len_list.keys():
        print("----------------------------------------")
        dat_filename = f"{src}WIFI-{mod}{ptn}dat"
        print(f"{dat_filename = }")

        pkt_len = pkt_len_list[mod]

        s = None
        e = None

        if args.i:
            s = 0
            e = INSPECT_LEN

        if os.path.isfile(dat_filename):
            print("is file")
            data = np.fromfile(dat_filename, dtype=np.complex64)
            print(data.shape)

            if s is None or e is None:
                s = 0
                e = data.shape[0]

            plot_data = data[s:e]
            trimmed_pkt = trim(plot_data, pkt_len, tx_pwr, mod)
            print(f"{trimmed_pkt.shape = }")

            save_dat_name = f"{src}Trimmed-WIFI-{mod}{ptn}dat"
            print(f"{save_dat_name = }")
            if args.i:
                trimmed_pkt.tofile(save_dat_name)
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

