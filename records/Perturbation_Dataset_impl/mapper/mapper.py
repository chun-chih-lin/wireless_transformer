import numpy as np
import matplotlib.pyplot as plt

def get_angle(sym):
    return np.angle(sym, deg=True)

# --------------------------------------------------------
# 0, 1
BPSK_SYMBOL=np.array([8.8752+0.0j, -8.8752+0.0j])
# 00, 10, 01, 11
QPSK_SYMBOL=np.array([6.2757+6.2757j, -6.2757+6.2757j, 6.2757-6.2757j, -6.2757-6.2757j])
# 0000, 0010, 0001, 0011, 1000, 1010, 1001, 1011, 0100, 0110, 0101, 0111, 1000, 1010, 1001, 1011
QAM16_SYMBOL=np.array([8.4197+8.4197j, 2.8065+8.4197j, 2.8065+2.8065, 8.4197+2.8065, \
              -8.4197+8.4197j, -2.8065+8.4197j, -2.8065+2.8065, -8.4197+2.8065, \
              -8.4197-8.4197j, -2.8065-8.4197j, -2.8065-2.8065, -8.4197-2.8065, \
              8.4197-8.4197j, 2.8065-8.4197j, 2.8065-2.8065, 8.4197-2.8065])

QAM64_SYMBOL=np.array([9.5863+9.6979j, 9.5863+6.8473j, 6.8473+6.8473j, 6.8473+9.6979j, \
              9.5863+4.1084j, 9.5863+1.3694j, 6.8473+1.3694j, 6.8473+4.1084j, \
              4.1084+4.1084j, 4.1084+1.3694j, 1.3694+1.3694j, 1.3694+4.1084j, \
              4.1084+9.5863j, 4.1084+6.8473j, 1.3694+6.8473j, 1.3694+9.6979j, \

              -9.5863+9.6979j, -9.5863+6.8473j, -6.8473+6.8473j, -6.8473+9.6979j, \
              -9.5863+4.1084j, -9.5863+1.3694j, -6.8473+1.3694j, -6.8473+4.1084j, \
              -4.1084+4.1084j, -4.1084+1.3694j, -1.3694+1.3694j, -1.3694+4.1084j, \
              -4.1084+9.5863j, -4.1084+6.8473j, -1.3694+6.8473j, -1.3694+9.6979j, \

              -9.5863-9.6979j, -9.5863-6.8473j, -6.8473-6.8473j, -6.8473-9.6979j, \
              -9.5863-4.1084j, -9.5863-1.3694j, -6.8473-1.3694j, -6.8473-4.1084j, \
              -4.1084-4.1084j, -4.1084-1.3694j, -1.3694-1.3694j, -1.3694-4.1084j, \
              -4.1084-9.5863j, -4.1084-6.8473j, -1.3694-6.8473j, -1.3694-9.6979j, \

              9.5863-9.6979j, 9.5863-6.8473j, 6.8473-6.8473j, 6.8473-9.6979j, \
              9.5863-4.1084j, 9.5863-1.3694j, 6.8473-1.3694j, 6.8473-4.1084j, \
              4.1084-4.1084j, 4.1084-1.3694j, 1.3694-1.3694j, 1.3694-4.1084j, \
              4.1084-9.5863j, 4.1084-6.8473j, 1.3694-6.8473j, 1.3694-9.6979j])

DECODE_IDX=[i for i in range(6, 33)] + [i for i in range(34, 60)]

def search_for_close(symbols, table):
    ret = [None]*len(symbols)

    for symbol_i in DECODE_IDX:
        symbol = symbols[symbol_i]
        if np.abs(symbol) < 0.1:
            continue
        symbol_array = np.repeat(symbol, len(table))
        distance = np.square(symbol_array.real - table.real)+np.square(symbol_array.imag - table.imag)
        decode = np.argmax(distance)

        ret[symbol_i] = decode
    return ret

# --------------------------------------------------------
def bpsk(sym):
    decode = search_for_close(sym, BPSK_SYMBOL)
    return decode

def qpsk(sym): 
    decode = search_for_close(sym, QPSK_SYMBOL)
    return decode

def qam16(sym): 
    decode = search_for_close(sym, QAM16_SYMBOL)
    return decode

def qam64(sym): 
    decode = search_for_close(sym, QAM64_SYMBOL)
    return decode

def int_array_to_bit_array(int_array, bit_num=1):
    ret = []
    for num in int_array:
        num = 0
        if bit_num == 1:
            for bit in f'{num:01b}':
                ret.append(bit)
        elif bit_num == 2:
            for bit in f'{num:02b}':
                ret.append(bit)
        elif bit_num == 4:
            for bit in f'{num:04b}':
                ret.append(bit)
        elif bit_num == 6:
            for bit in f'{num:08b}':
                ret.append(bit)
    return ret


