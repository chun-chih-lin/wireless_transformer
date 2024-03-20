import numpy as np
import sys, os, json


def clc_screen():
    ret = os.system('clear')
    if ret != 0:
        os.system('cls')

clc_screen()

def calculation_len(mod, pdu_l):
    try:
        with open('./search_tbl.json', 'r') as f:
            search_tbl = json.load(f)
        print(f"Mod: {mod}, Length: {pdu_l}")

        details = search_tbl[f"{mod}"]

        i = details['indent']
        p = details['pattern_start']
        s = details['start_n_symbol']

        print(f"{i = }, {p = }, {s = }")

        print(f"{len(i)}, {sum(i) = }")



        if pdu_l < p:
            t = s
            print(f"symbols = {t}")
        else:

            t = s + int((pdu_l - p)/sum(i))*len(i) + 1

            if mod == 1:
                r = 1
                print(f"{r = }")
                t += r
            print(f"symbols = {s} + ({pdu_l}-{p})/{sum(i)}*{len(i)} + 1 = {t}")
        

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
