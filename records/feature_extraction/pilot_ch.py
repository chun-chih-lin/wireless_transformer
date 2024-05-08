import numpy as np
from scipy import fft
import matplotlib.pyplot as plt
import os

N_FFT = 64
N_USED = 52
N_CP = 16

if os.system('clear') != 0:
    os.system('cls')

def main():
    data = np.fromfile('replayable_BPSK.dat', dtype=np.complex64)
    data_s = 100
    data_e = 1380

    # data = np.fromfile('replayable_QPSK.dat', dtype=np.complex64)
    # data_s = 100
    # data_e = 980
    
    data = np.fromfile('replayable_16QAM.dat', dtype=np.complex64)
    data_s = 100
    data_e = data_s + 640

    PILOT_LOC = [11, 25, 39, 53]    # The location after fftshift
    PILOT_VALUE = [1, 1, 1, -1]     # The value after fftshift
    # PILOT_LOC = [12, 26, 40, 54]

    data = data[data_s:data_e]

    if data_s == 0:
        plt.plot(data.real)
        plt.plot(data.imag)
        plt.show()
        exit()

    ttl_n_pkl = int(data.shape[0]/80)

    step = 50e-4
    t = np.array([x for x in np.arange(0, 64*step, step)]).astype(np.complex64)
    channel = np.exp(1j*t)
    print(f"{channel = }")

    for n_pkt in range(0, ttl_n_pkl):
        ori_pkt = data[n_pkt*80+16:(n_pkt+1)*80]

        tx_fft = np.fft.fftshift(np.fft.fft(ori_pkt))

        pkt = np.multiply(ori_pkt, channel)
        ch_fft = np.fft.fft(pkt)

        max_fft_pkt = np.max([np.max(np.abs(ch_fft.real)), np.max(np.abs(ch_fft.imag))])
        ori_fft_pkt = np.fft.fftshift(ch_fft/max_fft_pkt)

        temp = PILOT_VALUE/ori_fft_pkt[PILOT_LOC]
        x_slope = (temp[3] - temp[0]).real/43
        y_slope = (temp[3] - temp[0]).imag/43
        x_center = (temp[2] + temp[1]).real/2
        y_center = (temp[2] + temp[1]).imag/2

        # Compensate phase
        h_x = np.array([x+x_center for x in np.arange(0, x_slope*64, x_slope)])
        h_y = np.array([y+y_center for y in np.arange(0, y_slope*64, y_slope)])
        h = h_x + 1j*h_y

        # mean_temp = np.mean(temp)
        # print(temp, mean_temp)

        fft_pkt = ori_fft_pkt*h

        # plt.plot(tx_fft.real, color='tab:blue', linestyle='-')
        # plt.plot(tx_fft.imag, color='tab:red', linestyle='-.')
        # plt.plot(PILOT_LOC, tx_fft[PILOT_LOC].real, color='blue', linestyle='none', marker='o', markerfacecolor='none')
        # plt.plot(PILOT_LOC, tx_fft[PILOT_LOC].imag, color='red', linestyle='none', marker='o', markerfacecolor='none')
        # # plt.plot(ori_pkt.real, color='tab:gray', linestyle='-')
        # # plt.plot(ori_pkt.imag, color='tab:gray', linestyle='-.')
        # # plt.plot(pkt.real, color='tab:blue', linestyle='-')
        # # plt.plot(pkt.imag, color='tab:red', linestyle='-.')
        # # plt.plot(fft_pkt.real, color='tab:red', linestyle='-')
        # # plt.plot(fft_pkt.imag, color='tab:red', linestyle='-.')
        # # # plt.plot(h_x, color='g', linestyle='-')
        # # # plt.plot(h_y, color='g', linestyle='-.')
        # plt.plot(channel.real, color='black', linewidth=2, linestyle='-')
        # plt.plot(channel.imag, color='black', linewidth=2, linestyle='-.')

        # plt.plot(PILOT_LOC, temp.real, marker='o', markerfacecolor='none')
        # plt.plot(PILOT_LOC, temp.imag, marker='o', markerfacecolor='none')
        # # plt.plot(PILOT_LOC, fft_pkt[PILOT_LOC].real, color='b', marker='o', markerfacecolor='none')
        # # plt.plot(PILOT_LOC, fft_pkt[PILOT_LOC].imag, color='r', marker='o', markerfacecolor='none')
        # plt.show()

        plt.plot(tx_fft.real, tx_fft.imag, marker='o', color='tab:blue', markerfacecolor='none', linestyle='none')
        plt.plot(ch_fft.real, ch_fft.imag, marker='o', color='tab:red', markerfacecolor='none', linestyle='none')
        plt.plot(ori_fft_pkt.real, ori_fft_pkt.imag, marker='o', color='b', linestyle='none')
        plt.plot(fft_pkt.real, fft_pkt.imag, marker='o', color='r', linestyle='none')
        plt.show()
        # break



    # # Generate OFDM symbol
    # data = np.random.randint(0, 2, N_USED)  # Random binary data
    # symbol = np.zeros(N_FFT, dtype=complex)
    # symbol[np.arange(N_USED)] = data * 2 - 1  # QPSK modulation
    # symbol = np.fft.ifft(symbol)  # IFFT
    # symbol = np.concatenate([symbol[-N_CP:], symbol])  # Add cyclic prefix

    # # Channel fading
    # channel = np.random.randn(N_FFT + N_CP) + 1j * np.random.randn(N_FFT + N_CP)  # Complex Gaussian channel
    # received = symbol * channel  # Apply channel fading

    # # OFDM symbol recovery
    # received = received[N_CP:]  # Remove cyclic prefix
    # received_freq = np.fft.fft(received)  # FFT

    # # Channel estimation and equalization
    # pilots = np.arange(-21, 22, 7)+32  # Pilot subcarrier indices
    # print(f"{pilots = }")
    # H_pilots = received_freq[pilots]  # Channel response at pilot subcarriers

    # H_interp = np.fft.ifft(np.concatenate([H_pilots, np.zeros(N_FFT - N_USED)]))  # Interpolate channel response
    # H_interp = np.fft.fft(H_interp, N_FFT)  # FFT of interpolated channel response
    # equalized = received_freq / H_interp  # Equalization

    # # Demodulation
    # demod_data = np.round((np.real(equalized[np.arange(N_USED)]) + 1j * np.imag(equalized[np.arange(N_USED)])) / 2).astype(int)

    # # demod_data = np.array([1 if x > 0 else 0 for x in demod_data]).astype(int8)
    # print("Transmitted Data:", data)
    # print("Recovered Data:", demod_data)
    pass

if __name__ == '__main__':
    main()