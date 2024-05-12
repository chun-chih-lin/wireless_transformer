import sys, os
import argparse

if os.system("clear") != 0:
    os.system("cls")

parser = argparse.ArgumentParser(description='save torch experience file to npy.')
parser.add_argument('-s', '--source_folder', help='source torch experience file directory.', required=True)
parser.add_argument('-y', help='yes to all', action='store_true')
args = parser.parse_args()


def main():
    folders = os.listdir(args.source_folder)
    
    for folder in folders:
        print('-'*20)
        full_folder_path = f"{args.source_folder}{folder}"
        print(f"{full_folder_path = }")
        filenames = os.listdir(full_folder_path)
        for filename in filenames:
            print(f"{filenames = }")


    pass


if __name__ == '__main__':
    main()


