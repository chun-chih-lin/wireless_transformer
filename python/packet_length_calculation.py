import numpy as np
import sys, os, json


def clc_screen():
    ret = os.system('clear')
    if ret != 0:
        os.system('cls')

clc_screen()

SEARCH_TBL = {
    "0": {
        "indent": [3],
        "pattern_start": 3,
        "start_n_symbol": 16
    },
    "1": {
        "indent": [5, 4],
        "pattern_start": 1,
        "start_n_symbol": 12
    },
    "2": {
        "indent": [6],
        "pattern_start": 6,
        "start_n_symbol": 11
    },
    "3": {
        "indent": [9],
        "pattern_start": 6,
        "start_n_symbol": 9
    },
    "4": {
        "indent": [12],
        "pattern_start": 6,
        "start_n_symbol": 8
    },
    "5": {
        "indent": [18],
        "pattern_start": 6,
        "start_n_symbol": 7
    },
    "6": {
        "indent": [24],
        "pattern_start": 18,
        "start_n_symbol": 7
    },
    "7": {
        "indent": [27],
        "pattern_start": 24,
        "start_n_symbol": 7
    }
}



def calculation_len(mod, pdu_l):
    try:
        with open('./search_tbl.json', 'r') as f:
            search_tbl = json.load(f)
        # print(f"Mod: {mod}, Length: {pdu_l}")

        details = search_tbl[f"{mod}"]

        i = details['indent']
        p = details['pattern_start']
        s = details['start_n_symbol']

        if pdu_l < p:
            t = s
        else:
            t = s + int((pdu_l - p)/sum(i))*len(i) + 1

            if mod == 1:
                r = int(((pdu_l - p)%sum(i))/i[0])
                t += r
        return t*80


    except Exception as exp:
        e_type, e_obj, e_tb = sys.exc_info()
        print(f'Exception: {exp}. At line {e_tb.tb_lineno}')


def main():
    
    while True:

        cmd = input()

        if cmd.upper() == 'Q':
            print("Quitting.")
            break
        else:
            try:
                clc_screen()
                print(f"input: {cmd}")

                mod, pdu_len = [int(x) for x in cmd.split()]

                samp_len = calculation_len(mod, pdu_len)
                print(f"{samp_len = }")
                print("----------------------")

            except Exception as exp:
                e_type, e_obj, e_tb = sys.exc_info()
                print(f'Exception: {exp}. At line {e_tb.tb_lineno}')


if __name__ == "__main__":
    main()
