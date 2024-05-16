import numpy as np


def main():
    f1 = "./Dataset_EIB_3F_Hallway_0430/Dataset_EIB_3F_Hallway_0430_BT-GFSK-S2Coding_TP5_D15_SR5_CF2360_I0.dat"
    f2 = "./Dataset_EIB_3F_Hallway_0430/Dataset_EIB_3F_Hallway_0430_BT-GFSK-S8Coding_TP5_D15_SR5_CF2360_I0.dat"

    f1_data = np.fromfile(open(f1), dtype=np.complex64)
    f2_data = np.fromfile(open(f2), dtype=np.complex64)

    print(f1_data[0])
    print(f2_data[0])

    pass

if __name__ == '__main__':
    main()

