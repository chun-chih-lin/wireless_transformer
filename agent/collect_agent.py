import numpy as np
import redis as redis
import utils
import time
import json
import random
import string
import sys, os
# import socket
# import scapy.all as scapy

from BasicAgent import BasicAgent

class CollectAgent(BasicAgent):
    """docstring for CollectAgent"""
    def __init__(self, subprefix, agentkey):
        super(CollectAgent, self).__init__("CollectAgent", subprefix, agentkey, debug=True)
        self.d_msg('ActionAgent Initialization done.')

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
                self.db.get(db_key)
            else:
                self.d_msg(f"Get action: {action}")

        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            self.d_msg(f'Exception occurs: {exp}. At line {e_tb.tb_lineno}')
        pass

def main():
    print('Running Collect Agent...')
    CollectAgent('SYSTEM:COLLECT:*', 'AGENT:COLLECT')

if __name__ == "__main__":
    main()