#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 gr-wireless_dump author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
import pmt, sys
import redis
import threading
from time import sleep
import random, string

class generate_random_message(gr.sync_block):
    """
    docstring for block generate_random_message
    """
    def __init__(self, pattern, pdu_len, random, interval, num_msg):
        gr.sync_block.__init__(self,
            name="generate_random_message",
            in_sig=None,
            out_sig=None)
        self.set_pattern(pattern)
        self.set_pdu_len(pdu_len)
        self.set_random(random)
        self.set_interval(interval)
        self.set_num_msg(num_msg)

        self.is_busy = False

        self.set_db()
        self.message_port_register_out(pmt.string_to_symbol("out"))
        self.thread = threading.Thread(target=self.run_subscribe)

    def get_rand_message(self):
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=self.pdu_len))

    def set_pattern_message(self):
        self.p_message = "".join([self.pattern for i in range(self.pdu_len)])

    def generate_message(self):
        try:
            msg_count = 0
            while msg_count <= self.num_msg:
                print(f"Sending #{msg_count} Message.")
                if self.random:
                    # Generate random output message
                    msg = self.get_rand_message()
                else:
                    # Generate pattern output message
                    msg = self.p_message

                msg_count += 1
                self.message_port_pub(pmt.string_to_symbol("out"), pmt.intern(msg))
                sleep(self.interval)

        except Exception as exp:
        _, _, e_tb = sys.exc_info()
        print(f'[MSG Generator] Exception: {exp}, Line {e_tb.tb_lineno}')

    def event_handler(self, msg):
        try:
            if msg["data"].decode("utf-8") == "del":
                return

            key = msg["channel"].decode()
            split_key = key.split(":")
            db_key = ":".join([i for i in split_key[1:]])

            # Use:
            #   SET GENERATE_MSG:SEND True
            # To trigger sending message

            if db_key and not self.is_busy:
                # Prepare to generate messages
                if split_key[1] == "SEND" and self.db.get(db_key) == "True":
                    print("Sending message")
                    print("Set to be busy.")
                    self.is_busy = True
                    self.generate_message()
                    self.db.set(db_key, "False")
                    print("Reset to be not busy.")
                    self.is_busy = False
                else:
                    print(f"{db_key = }")


        except Exception as exp:
            _, _, e_tb = sys.exc_info()
            print(f'[MSG Generator] Exception: {exp}, Line {e_tb.tb_lineno}')
        pass

    def set_db(self):
        self.db = redis.Redis(host="localhost", port=6379, db=0)
        self.db.config_set('notify-keyspace-events', 'KEA')
        self.subprefix = f'__keyspace@0__'

    def run_subscribe(self):
        self.pubsub = self.db.pubsub()
        self.pubsub.psubscribe(**{self.subprefix+":GENERATE_MSG:*": self.event_handler})

    def set_pattern(self, pattern):
        self.pattern = pattern
        if hasattr(self, 'pdu_len'):
            self.set_pattern_message()
        
    def set_pdu_len(self, pdu_len):
        self.pdu_len = pdu_len
        if hasattr(self, 'pattern'):
            self.set_pattern_message()
        
    def set_random(self, random):
        self.random = random
        
    def set_interval(self, interval):
        self.interval = interval * 0.001

    def set_num_msg(self, num_msg):
        self.num_msg = num_msg

    def work(self, input_items, output_items):
        return False
