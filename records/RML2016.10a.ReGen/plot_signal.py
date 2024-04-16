import numpy as np
import os, sys
import matplotlib.pyplot as plt

if os.system('clear') != 0:
    os.system('cls')

def main():
    print(sys.argv)
    if len(sys.argv) == 2:
        dat_filename = f"WIFI-{sys.argv[1]}.dat"
        if os.path.isfile(dat_filename):
            print("is file")
            data = np.fromfile(dat_filename, dtype=np.complex64)
            print(data.shape)


            #plt.plot(data.real)
            #plt.plot(data.imag)
            #plt.show()


        else:
            print("not a file")



if __name__ == "__main__":
    main()

