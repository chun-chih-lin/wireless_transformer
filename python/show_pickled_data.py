import _pickle as pickle
import numpy as np
import sys, os, json
import matplotlib.pyplot as plt
import redis

ret = os.system("clear")
if ret != 0:
    os.system("cls")



def main():
    db = redis.StrictRedis(host="localhost", port=6379, db=0)

    keys = db.keys("*:WIFI:*:1")
    


    for key in keys:
        print(key.decode())
        unpacked_obj = pickle.loads(db.get(key))
        print(unpacked_obj[0])
        unpacked_obj= unpacked_obj[:700]
        plt.plot([i for i in range(unpacked_obj.shape[0])], unpacked_obj.real)
        plt.plot([i for i in range(unpacked_obj.shape[0])], unpacked_obj.imag)
        # break

    plt.show()
    pass

if __name__ == '__main__':
    main()
