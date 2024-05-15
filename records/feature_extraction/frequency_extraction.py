import numpy as np
import matplotlib.pyplot as plt

def get_dft_matrix(N=64, M=1):
    dft_mtx = np.expand_dims(np.fft.fft(np.eye(N)), axis=0)
    return np.repeat(dft_mtx, M, axis=0)

def dft(input_ary, N=64, batch_size=10_000, preprint=""):
    n_batch = int(input_ary.shape[0]/batch_size) + 1

    dft_mtx = get_dft_matrix(N=N, M=batch_size)

    dft_ret = None
    for n_b in range(n_batch):
        print(f"{preprint}Batch [{n_b}/{n_batch}]...")
        if (n_b+1)*batch_size <= input_ary.shape[0]:
            batch_ary = input_ary[n_b*batch_size:(n_b+1)*batch_size, :]
        else:
            batch_ary = input_ary[n_b*batch_size:, :]
            dft_mtx = get_dft_matrix(N=N, M=input_ary.shape[0]-n_b*batch_size)

        sub_dft_ret = np.matmul(batch_ary, dft_mtx)
        if dft_ret is None:
            dft_ret = sub_dft_ret
        else:
            dft_ret = np.concatenate((dft_ret, sub_dft_ret), axis=0)
    return dft_ret

def freq_offset(ary):
    PILOT_LOC = [11, 25, 39, 53]
    PILOT_VALUE = np.array([1j, -1j, 1j ,1j])

    phase_offset = np.divide(PILOT_VALUE, ary[:, :, PILOT_LOC])

    print(f"{phase_offset.shape = }")
    avg_phase_offset = np.expand_dims(np.mean(phase_offset, axis=2), axis=2)
    print(f"{avg_phase_offset.shape = }")
    print(f"{ary.shape = }")
    ret = np.multiply(ary, np.repeat(avg_phase_offset, 64, axis=2))
    print(f"{ret.shape = }")
    print(ret[0, :, PILOT_LOC])
    return ret
    pass

def frequency_extraction(input_ary, N=64, indent=8):

    if len(input_ary.shape) == 2:
        input_ary = np.expand_dims(input_ary, axis=0)

    complex_input = input_ary[:, 0, :] + 1.0j*input_ary[:, 1, :]

    num_pkt = complex_input.shape[0]
    time_indent_len = int(N/indent)
    ttl_dft_mtx_ret = np.zeros((num_pkt, time_indent_len, N), dtype=np.complex64)

    for i, idx in enumerate(range(0, N, indent)):
        print(f"[{i}/{time_indent_len}]", end="  ")
        cyclic_complex_input = np.roll(complex_input, i*indent, axis=1)
        sub_ary = np.expand_dims(cyclic_complex_input[:, :N], axis=1)
        dft_mtx_ret = dft(sub_ary, N=N, preprint=f"[{i}/{time_indent_len}]  ")

        ttl_dft_mtx_ret[:, i, :] = np.fft.fftshift(np.squeeze(dft_mtx_ret), axes=(1, ))

    # print(f"{ttl_dft_mtx_ret.shape = }")
    # ttl_dft_mtx_ret = freq_offset(ttl_dft_mtx_ret)
    return ttl_dft_mtx_ret
    pass

def inspect_freq(freq_ret, ret_label, ret_mod, show=False):
    print("Inspecting frequency retults")
    print(f"\t{freq_ret.shape = }")
    if not show:
        return

    cmap = plt.get_cmap('turbo')
    axis_lim = 1.5
    colors = [cmap(i) for i in np.linspace(0, 1, freq_ret.shape[1])]
    num_pkt = freq_ret.shape[0]
    for pkt_i in range(num_pkt):
        label = ret_label[pkt_i]
        mod_name = ret_mod[label]

        fig, ax = plt.subplots()
        ax.matshow(np.abs(freq_ret[pkt_i, :, :]))
        ax.set_axis_off()
        # plt.savefig(f"{mod_name}-freq.png",bbox_inches='tight')

        # plt.figure(pkt_i)
        # fig, axs = plt.subplots(2, 1)
        # axs[0].matshow(np.abs(freq_ret[pkt_i, :, :]))
        # for indent in range(freq_ret.shape[1]):
        #     axs[1].plot(np.real(freq_ret[pkt_i, indent, :]), 
        #                 np.imag(freq_ret[pkt_i, indent, :]), 
        #                 linestyle='None', 
        #                 markersize=4, 
        #                 marker='o', 
        #                 markerfacecolor='none', 
        #                 color=colors[indent])
        # axs[1].set_aspect('equal')
        # axs[1].set_xlim(-axis_lim, axis_lim)
        # axs[1].set_ylim(-axis_lim, axis_lim)
        # plt.title(f"Freq: {mod_name}")
    plt.show()
    pass