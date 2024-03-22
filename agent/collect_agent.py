import numpy as np
import redis as redis
import utils
import time
import json
import random
import string
import sys, os
from datetime import datetime
import _pickle as pickle
# import socket
# import scapy.all as scapy

from BasicAgent import BasicAgent

class CollectAgent(BasicAgent):
    """docstring for CollectAgent"""
    def __init__(self, subprefix, agentkey):
        super(CollectAgent, self).__init__("CollectAgent", subprefix, agentkey, debug=True)
        self.d_msg('ActionAgent Initialization done.')

        self.patch_key = "CURRENT_PATCH"
        self.check_patch_name()

        self.cur_num_patch_key = "CURRENT_NUM_PATCH"
        self.check_patch_count()


    def agent_event_handler(self, msg):
        try:
            key = self.utf8_decode(msg['channel'])
            if key:
                db_key = self.utf8_decode(self.db.get(self.agentkey))
                if db_key == self.c["KEYWORD_QUIT"]:
                    self.d_msg('Quiting CollectAgent. See you again.')
                    self.db.set('AGENT:COLLECT', self.c["KEYWORD_STOP"])
                    self.thread.stop()
        except Exception as exp:
            self.d_msg(f'Exception occurs: {exp}')

    def event_handler(self, msg):
        try:
            # self.d_msg(f"event handler: {msg}")
            db_key = self.get_key(msg)
            action = self.get_action(msg)
            data = self.get_db_data(msg)
            # self.d_msg(f"{db_key = }")
            if data == 'del':
                # Nothing for del operation for now.
                pass
            else:
                if action == "DEBUG":
                    self.d_msg(f"Get action: {action}")
                    self.update_debug(db_key)
                    
                elif action == "WIFI":
                    self.d_msg(f"Collecting a WiFi packet")
    
                    self.d_msg("Increment the count by 1")
                    self.increment_patch_count()
                else:
                    self.d_msg(f"Get action: {action}")

        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            self.d_msg(f'Exception occurs: {exp}. At line {e_tb.tb_lineno}')
        pass

    # --------------------------------------------------------------
    def update_debug(self, db_key):
        try:
            d = self.db.get(db_key).decode()
            if d == "True":
                self.debug = True
            elif d == "False":
                self.debug = False

        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            self.d_msg(f'Exception occurs: {exp}. At line {e_tb.tb_lineno}')
        pass

    # --------------------------------------------------------------

    def get_new_patch_name(self):
        now = datetime.now()
        formatted = now.strftime("%Y_%m_%d_%H_%M_%S")
        return formatted

    def check_patch_name(self):
        try:
            if not self.db.exists(self.patch_key):
                new_patch_name = self.get_new_patch_name()
                self.db.set(self.patch_key, new_patch_name)
                self.cur_patch_name = new_patch_name
            else:
                self.cur_patch_name = self.db.get(self.patch_key).decode()
        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            self.d_msg(f'Exception occurs: {exp}. At line {e_tb.tb_lineno}')

    def increment_patch_count(self):
        self.db.incr(self.cur_num_patch_key)
        self.check_patch_count()

    def check_patch_count(self):
        try:
            if not self.db.exists(self.cur_num_patch_key):
                self.db.set(self.cur_num_patch_key, 0)
            else:
                cur_n = int(self.db.get(self.cur_num_patch_key).decode())
                if cur_n >= self.c["MAX_PATCH_NUM"]:
                    # Reach the MAX number, pack data to file
                    self.db.set(self.cur_num_patch_key, 0)
                    self.pack_data()
                    # Update the new patch name
                    self.d_msg(f"Counter to the max. New patch name.")
                    self.cur_patch_name = self.get_new_patch_name()
                    self.db.set(self.patch_key, self.cur_patch_name)
        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            self.d_msg(f'Exception occurs: {exp}. At line {e_tb.tb_lineno}')


    # --------------------------------------------------------------
    def pack_data(self):
        try:
            # Collecting all data to the dataset.
            current_mod = None
            dataset = None

            patch_key_p = f"{self.subprefix}:{self.cur_patch_name}:*"

            for key in self.db.scan_iter(patch_key_p):
                if current_mod is None:
                    current_mod = key.decode().split(":")
                value = pickle.loads(self.db.get(key))
                r_part = np.expand_dims(np.real(value), axis=0)
                i_part = np.expand_dims(np.imag(value), axis=0)

                two_ch_value = np.concatenate((r_part, i_part), axis=0).reshape(1, 2, r_part.shape[1])
                if dataset is None:
                    dataset = two_ch_value
                else:
                    dataset = np.append(dataset, two_ch_value, axis=0)

            
            # Save the dataset to a pickle file
            mod_mcs = int(current_mod[3])
            mod_str = self.c["MOD_INFO"][current_mod[2]][current_mod[3]]["Modulation"]
            mod_codr = self.c["MOD_INFO"][current_mod[2]][current_mod[3]]["CodingRate"]
            
            dataset_dict = {
                (mod_str, mod_mcs): dataset
            }

            save_dataset_name = f"{mod_str}.{mod_mcs}.{self.cur_patch_name}.pkl"

            self.d_msg(f"save {dataset_dict = }")
            with open(f"{self.c['SAVE_DIRECTORY']}{save_dataset_name}", 'wb') as f:
                pickle.dump(dataset_dict, f)
                pass

            # Register the information to the file.
            save_filename = f"{self.c['SAVE_DIRECTORY']}{self.c['PATCH_INFO_FILENAME']}"
            self.d_msg(f"Packing data to file: {save_filename}")
            save_description = "Description"

            if os.path.isfile(save_filename):
                with open(save_filename) as f:
                    file_info = json.load(f)
            else:
                file_info = {}

            file_info[self.cur_patch_name] = {
                    "MCS": mod_mcs,
                    "CodingRate": mod_codr,
                    "MOD": mod_str
            }

            with open(save_filename, 'w') as f:
                json.dump(file_info, f, indent=4)

            # delete the key of the patch
            self.del_key_pattern(patch_key_p)
        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            self.d_msg(f'Exception occurs: {exp}. At line {e_tb.tb_lineno}')

    def del_key_pattern(self, key_p):
        for key in self.db.scan_iter(key_p):
            self.db.delete(key)

    # --------------------------------------------------------------

def main():
    print('Running Collect Agent...')

    CollectAgent('SYSTEM:COLLECT:*', 'AGENT:COLLECT')

if __name__ == "__main__":
    main()
