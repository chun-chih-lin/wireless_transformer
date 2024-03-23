import _pickle as pickle
import os, sys
import json
from datetime import datetime

def main():
    try:
        now = datetime.now()
        bz2_filename = now.strftime("%Y_%m_%d_%H_%M_%S")
        folder_name = f"./wireless_data/{bz2_filename}"
        os.mkdir(folder_name)
    
        with open("./wireless_data/patch_info.json", 'r') as f:
            all_file_details = json.load(f)
    
        for detail in all_file_details.keys():
            print(f"{detail = }")
            filename = all_file_details[detail]["Filename"]
            os.system(f"cp ./wireless_data/{filename} {folder_name}")
    
        # os.system("tar -cvjSf {folder_name}.tar.bz2 {folder_name}")
    except Exception as exp:
        e_type, e_obj, e_tb = sys.exc_info()
        print(f'Exception occurs: {exp}. At line {e_tb.tb_lineno}')



if __name__ == "__main__":
    main()
