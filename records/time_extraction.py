import numpy as np
import matplotlib.pyplot as plt


def corrmtx(input_ary, N=64):
    H1 = np.expand_dims(input_ary, axis=1)
    H2 = np.flip(H1, 2)

    H1 = H1[:, :, 0:N]
    H2 = H2[:, :, 0:N]

    H = np.concatenate((H2, H1), axis=1)/np.sqrt(2)
    R = np.matmul(np.transpose(H.conj(), axes=(0, 2, 1)), H)
    return R

def time_extraction(input_ary, indent=8):
    if len(input_ary.shape) == 2:
        input_ary = np.expand_dims(input_ary, axis=0)

    complex_input = input_ary[:, 0, :] + 1.0j*input_ary[:, 1, :]

    num_pkt = complex_input.shape[0]
    sub_ary_len = int(complex_input.shape[1]/2)
    N = int(sub_ary_len/2)

    ttl_corrmtx_ret_shape = (num_pkt, int(sub_ary_len/indent), N, N)
    ttl_corrmtx_ret = np.zeros(ttl_corrmtx_ret_shape, dtype=np.complex64)

    for i, idx in enumerate(range(0, sub_ary_len, indent)):
        ret = corrmtx(complex_input[:, idx:idx+sub_ary_len], N=N)
        ttl_corrmtx_ret[:, i, :, :] = ret
        # break

    print(f"{ttl_corrmtx_ret.shape = }")
    # fig, axs = plt.subplots(2, 2)
    # axs[0, 0].matshow(np.abs(ttl_corrmtx_ret[0, 0, :, :]))
    # axs[0, 1].matshow(np.abs(ttl_corrmtx_ret[0, 1, :, :]))
    # axs[1, 0].matshow(np.abs(ttl_corrmtx_ret[0, 2, :, :]))
    # axs[1, 1].matshow(np.abs(ttl_corrmtx_ret[0, 3, :, :]))

    return ttl_corrmtx_ret.reshape((num_pkt, 64, 64))
    pass

def inspect_time(time_ret, ret_label, ret_mod):
    print(f"Inspecting time retults, {time_ret.shape = }")
    num_pkt = time_ret.shape[0]
    for pkt_i in range(num_pkt):
        label = ret_label[pkt_i]
        mod_name = ret_mod[label]
        # plt.matshow(np.abs(time_ret[pkt_i, :, :]))
        # plt.show()
