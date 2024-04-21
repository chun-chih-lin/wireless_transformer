import numpy as np
import matplotlib.pyplot as plt

def get_dft_matrix(N=64, M=1):
    dft_mtx = np.expand_dims(np.fft.fft(np.eye(N)), axis=0)
    return np.repeat(dft_mtx, M, axis=0)

def create_shift_sub_ary():
    pass

def frequency_extraction(input_ary):
    if len(input_ary.shape) == 2:
        input_ary = np.expand_dims(input_ary, axis=0)
        
    complex_input = input_ary[:, 0, :] + 1.0j*input_ary[:, 1, :]

    num_pkt = complex_input.shape[0]
    sub_ary_len = int(complex_input.shape[1]/2)

    dft_mtx = get_dft_matrix(N=sub_ary_len, M=num_pkt)

    ttl_dft_mtx_ret = np.zeros((num_pkt, sub_ary_len, sub_ary_len), dtype=np.complex64)

    for i in range(sub_ary_len):
        sub_ary = np.expand_dims(complex_input[:, i:i+sub_ary_len], axis=1)
        dft_mtx_ret = np.matmul(sub_ary, dft_mtx)
        ttl_dft_mtx_ret[:, i, :] = np.squeeze(dft_mtx_ret)

    return ttl_dft_mtx_ret
    pass

def inspect_freq(freq_ret, ret_label, ret_mod):
    print("Inspecting frequency retults")
    num_pkt = freq_ret.shape[0]
    for pkt_i in range(num_pkt):
        label = ret_label[pkt_i]
        mod_name = ret_mod[label]
        # plt.matshow(np.abs(freq_ret[pkt_i, :, :]))
        # plt.title(mod_name)
        # plt.show()
    pass