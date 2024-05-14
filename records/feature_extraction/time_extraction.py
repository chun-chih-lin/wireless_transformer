import numpy as np
import matplotlib.pyplot as plt


def corrmtx(input_ary, N=64, batch_size=10_000, preprint=""):
    n_batch = int(input_ary.shape[0]/batch_size) + 1
    R = None
    for n_b in range(n_batch):
        print(f"{preprint}Batch [{n_b}/{n_batch}]...")
        if (n_b+1)*batch_size <= input_ary.shape[0]:
            batch_ary = input_ary[n_b*batch_size:(n_b+1)*batch_size, :]
        else:
            batch_ary = input_ary[n_b*batch_size:, :]

        H1 = np.expand_dims(batch_ary, axis=1)
        H2 = np.flip(H1, 2)

        H1 = H1[:, :, 0:N]
        H2 = H2[:, :, 0:N]

        H = np.concatenate((H2, H1), axis=1)/np.sqrt(2)
        _R = np.matmul(np.transpose(H.conj(), axes=(0, 2, 1)), H)


        if R is None:
            R = _R
        else:
            R = np.concatenate((R, _R), axis=0)
    return R

def time_extraction(input_ary, indent=8):
    if len(input_ary.shape) == 2:
        input_ary = np.expand_dims(input_ary, axis=0)

    complex_input = input_ary[:, 0, :] + 1.0j*input_ary[:, 1, :]

    num_pkt = complex_input.shape[0]
    sub_ary_len = int(complex_input.shape[1]/2)
    N = int(sub_ary_len/4)

    time_indent_len = int(sub_ary_len/indent)

    ttl_corrmtx_ret_shape = (num_pkt, time_indent_len, N, N)
    ttl_corrmtx_ret = np.zeros(ttl_corrmtx_ret_shape, dtype=np.complex64)

    for i, idx in enumerate(range(0, sub_ary_len, indent)):
        # print(f"[{i}/{time_indent_len}]  ", end="  ")
        ret = corrmtx(complex_input[:, idx:idx+sub_ary_len], N=N, preprint=f"[{i}/{time_indent_len}]  ")
        ttl_corrmtx_ret[:, i, :, :] = ret
        # break

    print(f"{ttl_corrmtx_ret.shape = }")
    # fig, axs = plt.subplots(2, 2)
    # axs[0, 0].matshow(np.abs(ttl_corrmtx_ret[0, 0, :, :]))
    # axs[0, 1].matshow(np.abs(ttl_corrmtx_ret[0, 1, :, :]))
    # axs[1, 0].matshow(np.abs(ttl_corrmtx_ret[0, 2, :, :]))
    # axs[1, 1].matshow(np.abs(ttl_corrmtx_ret[0, 3, :, :]))

    return ttl_corrmtx_ret.reshape((num_pkt, time_indent_len*N, N))
    pass

def inspect_time(time_ret, ret_label, ret_mod, show=False):
    print(f"Inspecting time retults")
    print(f"\t{time_ret.shape = }")
    if not show:
        return
    num_pkt = time_ret.shape[0]
    for pkt_i in range(num_pkt):
        label = ret_label[pkt_i]
        mod_name = ret_mod[label]

        fig, ax = plt.subplots()
        plt.figure(pkt_i)
        ax.matshow(np.abs(time_ret[pkt_i, :, :]))
        # ax.set_axis_off()
        # plt.savefig(f"{mod_name}-time.png",bbox_inches='tight')
        plt.title(f"Time: {mod_name}")
    plt.show()
