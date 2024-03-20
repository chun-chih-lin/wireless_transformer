import redis
import pickle
import sys, os
import numpy as np

ret = os.system("clear")
if ret != 0:
    os.system("cls")


def main():

    db = redis.StrictRedis(host="localhost", port=6379, db=0)
    unpacked_obj = pickle.loads(db.get("TEST_KEY"))
    print(f"{unpacked_obj = }, {unpacked_obj.shape}")


    key_list = db.keys("WIRELESS_PACKET:WIFI:*")
    for key in key_list:
        print(f"{key = }")
        unpacked_obj = pickle.loads(db.get(key))
        print(f"{unpacked_obj = }")
        print("\n****************\n")



    pass

if __name__ == "__main__":
    main()
