import numpy as np
import redis as redis
import utils
import time
import json
import random
import string
import sys, os
from datetime import datetime
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
            self.d_msg(f"event handler: {msg}")
            db_key = self.get_key(msg)
            action = self.get_action(msg)
            self.d_msg(f"{db_key = }")
            if action == "DEBUG":
                self.d_msg(f"Get action: {action}")
                d = self.db.get(db_key).decode()
                if d == "True":
                    self.debug = True
                elif d == "False":
                    self.debug = False
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
                    self.db.set(self.cur_num_patch_key, 0)
                    # TODO update the current patch name
                    new_patch_name = self.get_new_patch_name()
                    self.db.set(self.patch_key, new_patch_name)
                    self.d_msg(f"Counter to the max. New patch name: {new_patch_name}")
        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            self.d_msg(f'Exception occurs: {exp}. At line {e_tb.tb_lineno}')


def main():
    print('Running Collect Agent...')
    CollectAgent('SYSTEM:COLLECT:*', 'AGENT:COLLECT')

if __name__ == "__main__":
    main()
