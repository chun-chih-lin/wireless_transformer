import numpy as np
import sys, os
import _pickle as pickle
import matplotlib.pyplot as plt


LABEL_FONT_SIZE = 15.0

def plot_noise(noise, title):
    fig, ax = plt.subplots(layout='constrained')

    ax.plot(np.real(noise))
    ax.plot(np.imag(noise))

    # ax.set_xlabel('Sample', fontsize=LABEL_FONT_SIZE)
    ax.get_xaxis().set_ticklabels([])
    ax.set_ylabel('Amplitude', fontsize=LABEL_FONT_SIZE)
    ax.set_title(title, fontsize=15.0)
    ax.grid(linestyle='-', linewidth=.5)
    ax.set_xlim(0, 128)
    ax.set_ylim(-0.0025, 0.0025)

    fig.set_size_inches(6.5, 2.4)
    fig.show()
    return fig
    pass

def main():
    dat_filename = "Non_process_Dataset_EIB_Outdoor_pert_RAND_TP-10_D5_SR20_CF2360_I0.dat"
    pkl_filename = "Dataset_EIB_Outdoor_TP-10_D5_SR20_CF2360_I0.pkl"

    dat_data = np.fromfile(open(dat_filename), dtype=np.complex64)
    dat_data = dat_data.reshape((20_000, 128))

    with open(pkl_filename, 'rb') as f:
        pkl_data = pickle.load(f, encoding='latin1')


    print(f"{dat_data.shape = }")
    print(f"{pkl_data['X'].shape = }")

    pert_noise = dat_data[10, :]
    ori_noise_ch2 = pkl_data['X'][-1, :, :]

    ori_noise = ori_noise_ch2[0, :] + 1.0j*ori_noise_ch2[1, :]

    print(f"{pert_noise.shape = }, {type(pert_noise[0])}")
    print(f"{ori_noise.shape = }, {type(ori_noise[0])}")


    pert_noise_fig = plot_noise(pert_noise, title="Noise w/ Perturbation")
    ori_noise_fig = plot_noise(ori_noise, title="Noise w/o Perturbation")

    pert_noise_fig.savefig("pert_noise_fig.png", bbox_inches='tight')
    pert_noise_fig.savefig("pert_noise_fig.pdf", bbox_inches='tight')

    ori_noise_fig.savefig("ori_noise_fig.png", bbox_inches='tight')
    ori_noise_fig.savefig("ori_noise_fig.pdf", bbox_inches='tight')

    plt.show()
    pass

if __name__ == '__main__':
    main()