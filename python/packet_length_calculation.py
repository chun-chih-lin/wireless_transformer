import numpy as np
import sys, os, json

ret = os.system('clear')
if ret != 0:
    os.system('cls')



def calculation_len(mod, pdu_l):
    with open('./search_tbl.json', 'r') as f:
        search_tbl = json.load(f)
    try:
        print(f"Mod: {mod}, Length: {pdu_l}")


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

                print(f"input: {cmd}")

                mod, pdu_len = [int(x) for x in cmd.split()]

                samp_len = calculation_len(mod, pdu_len)

            except Exception as exp:
                e_type, e_obj, e_tb = sys.exc_info()
                print(f'Exception: {exp}. At line {e_tb.tb_lineno}')


if __name__ == "__main__":
    main()
