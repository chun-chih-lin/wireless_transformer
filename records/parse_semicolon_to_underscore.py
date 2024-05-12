import sys, os
import argparse

if os.system("clear") != 0:
    os.system("cls")

parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', '--source_folder', help='source torch experience file directory.', required=True)
parser.add_argument('-y', help='yes to all', action='store_true')
args = parser.parse_args()


# python parse_simicolon_to_underscore.py -s /home/chunchi/Desktop/models/
# convert all the ":" in filenames under the given 'models' folders to "_"

def main():
    folders = os.listdir(args.source_folder)
    
    for folder in folders:
        print('-'*20)
        full_folder_path = f"{args.source_folder}{folder}"
        print(f"{full_folder_path = }")
        filenames = os.listdir(full_folder_path)
        for filename in filenames:
            new_filename = filename.replace(":", "_")
            old_full_filename = f"{full_folder_path}/{filename}"
            new_full_filename = f"{full_folder_path}/{new_filename}"
            print(f"{old_full_filename = }")
            print(f"{new_full_filename = }")
            os.rename(old_full_filename, new_full_filename)
    pass


if __name__ == '__main__':
    main()


