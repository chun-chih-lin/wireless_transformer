import _pickle as pickle
import numpy as np
import os, sys

import matplotlib.pyplot as plt

if os.system("clear") != 0:
    os.system("cls")



def main():
    filename = "Dataset_EIB_room328_to_Hallway_TP-10_D5_SR20_CF2360_I0.pkl.npy"

    with open(filename, 'rb') as f:
        data = np.load(f, allow_pickle=True)

    print(data.shape)


    data_mean = np.mean(data, axis=0)
    data_average = np.average(data, axis=0)
    data_std = np.std(data, axis=0)
    data_var = np.var(data, axis=0)

    complex_mean = data_mean[0, :] + 1.0j*data_mean[1, :]
    complex_std = data_std[0, :] + 1.0j*data_std[1, :]
    fft_mean = np.fft.fftshift(np.fft.fft(complex_mean, n=64))
    fft_std = np.fft.fftshift(np.fft.fft(complex_std, n=64))

    
    fig, ax = plt.subplots(2, 2)
    ax[0, 0].plot(data_mean[0, :])
    ax[0, 0].plot(data_mean[1, :])
    ax[0, 0].set_title("mean")
    ax[0, 1].plot(data_std[0, :])
    ax[0, 1].plot(data_std[1, :])
    ax[0, 1].set_title("std")
    ax[1, 0].plot(np.real(fft_mean))
    ax[1, 0].plot(np.imag(fft_mean))
    ax[1, 0].set_title("mean")
    ax[1, 1].plot(np.real(fft_std))
    ax[1, 1].plot(np.imag(fft_std))
    ax[1, 1].set_title("std")

    plt.figure("Error Bor")
    plt.errorbar([x for x in range(128)], data_mean[0, :], data_std[0, :], \
        linestyle='none', fmt='o')
    plt.errorbar([x for x in range(128)], data_mean[1, :], data_std[1, :], \
        linestyle='none', fmt='o')


    plt.figure('Perturbation Waveform')
    for pkt_i in range(data.shape[0]):
        pkt = data[pkt_i, :, :]
        plt.plot(pkt[0, :], \
            linestyle="-")
        plt.plot(pkt[1, :], \
            linestyle=":")
        plt.show()
        break

    pass

if __name__ == '__main__':
    main()