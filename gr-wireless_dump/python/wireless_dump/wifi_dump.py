#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 gr-wireless_dump author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr
import pmt, json, sys
import redis
import _pickle as pickle

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

CURRENT_PATCH="CURRENT_PATCH"
CURRENT_NUM_PATCH="CURRENT_NUM_PATCH"

class wifi_dump(gr.sync_block):
    """
    docstring for block wifi_dump
    """
    def __init__(self, mod, pdu_len, debug):
        gr.sync_block.__init__(self,
            name="wifi_dump",
            in_sig=[np.complex64],
            out_sig=None)
        self.count = 0
        self.wifi_signal = None
        self.detect = False
        self.pdu_len = None

        self.db = redis.Redis(host='localhost', port=6379, db=0)

        self.set_debug(debug)
        self.set_modulation(mod)
        self.set_pdu_len(pdu_len)

        self.system_prefix_key = "SYSTEM:COLLECT:WIFI"

        self.input_c = 0
        self.tag_pos = []

        

    def d_msg(self, msg):
        if self.debug:
            print(msg)
    
    # ----------------------------------------------
    # Callback functions
    def set_modulation(self, mod):
        self.mod = mod
        if self.pdu_len is not None:
            self.update_ttl_sample()
        
    def set_pdu_len(self, pdu_len):
        self.pdu_len = pdu_len
        self.update_ttl_sample()

    def set_debug(self, debug):
        self.debug = debug
        print(f"Setting self.debug: {self.debug}")

    # ----------------------------------------------
    def update_ttl_sample(self):
        self.d_msg("Updating wifi signal length...")
        self.d_msg(f"{self.pdu_len = }, {self.mod = }")
        try:
            search_tbl = SEARCH_TBL
            details = search_tbl[f"{self.mod}"]

            i = details['indent']
            p = details['pattern_start']
            s = details['start_n_symbol']

            if self.pdu_len < p:
                t = s
            else:
                t = s + int((self.pdu_len - p)/sum(i))*len(i) + 1

                if self.mod == 1:
                    r = int(((self.pdu_len - p)%sum(i))/i[0])
                    t += r
            self.max_sample = t*80
            self.d_msg(f"Update sample to {self.max_sample}")

        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            self.d_msg(f'Exception: {exp}. At line {e_tb.tb_lineno}')

    def save_to_db(self, save_ary):
        try:
            pickled_obj = pickle.dumps(save_ary)

            set_key = f"{self.system_prefix_key}:TEST_KEY"
            if self.db.exists(CURRENT_PATCH) and self.db.exists(CURRENT_NUM_PATCH):
                patch_indicator = self.db.get(CURRENT_PATCH).decode()
                number = self.db.get(CURRENT_NUM_PATCH).decode()

                set_key = f"{self.system_prefix_key}:{self.mod}:{self.pdu_len}:{patch_indicator}:{number}"
                self.d_msg(f"Saving to Patch keys: {set_key}")
            else:
                self.d_msg(f"Patch keys do not exist. Using default key: {set_key}")

            self.db.set(set_key, pickled_obj)

        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            self.d_msg(f'Exception: {exp}. At line {e_tb.tb_lineno}')

    def get_tag_info(self, tags, tgt_name="wifi_start"):
        for tag in tags:
            tag_key = pmt.to_python(tag.key)
            if tag_key == tgt_name:
                tag_offset = tag.offset
                return tag_offset
        return None


    def work(self, input_items, output_items):
        try:
            in0 = input_items[0]
            tags = self.get_tags_in_window(0, 0, len(input_items[0]))

            # ------
            # Get all the samples have wifi_start as tag name
            if len(tags) > 0:
                for tag in tags:
                    if pmt.to_python(tag.key) == 'wifi_start':
                        self.tag_pos.append(tag.offset - self.nitems_read(0))
                self.tag_pos.sort()

            print("===============================")
            print(f"{len(in0) = }")
            for n in range(len(self.tag_pos)):
                print(self.tag_pos.pop())


            # ------
            i = 0
            while False:
                print('.')
                if not self.detect:
                    # I have not detect anything yet.
                    # Check if there is any tag that I'm interested in.
                    if len(self.tag_pos) > 0:
                        print("Detected something.")
                        # Something interesting is in the list
                        # Set to detected
                        self.detect = True

                        # Store the interested wifi signal
                        # Only store the predefined length
                        offset_sample = self.tag_pos.pop(0)
                        i += offset_sample

                        store_len = min(len(in0) - offset_sample, self.max_sample)
                        i += store_len

                        print(f"{offset_sample = }, {store_len = }")

                        self.wifi_signal = in0[offset_sample:offset_sample + store_len]
                        if len(self.wifi_signal) < self.max_sample:
                            # Not a complete packet.
                            print("Not a complete packet. Keep waiting for more samples.")
                            pass
                        else:
                            # it is a complete packet already.
                            # Export the result
                            self.input_c += 1
                            print(f"Complete! [#{self.input_c}] Save packet: {len(self.wifi_signal) = }")
                            self.wifi_signal = None
                            # Reset to not detecting
                            self.detect = False
                else:
                    # I have detected something already.
                    print("Detected something already.")
                    store_len = min(len(in0), self.max_sample - len(self.wifi_signal))
                    i += store_len

                    self.wifi_signal = np.concatenate((self.wifi_signal, in0[:store_len]))
                    if len(self.wifi_signal) < self.max_sample:
                        # Not a complete packet.
                        print("Not a complete packet. Keep waiting for more samples.")
                        pass
                    else:
                        # it is a complete packet already.
                        # Export the result
                        print(f"Fianlly Complete! [#{self.input_c}] Save packet: {len(self.wifi_signal) = }")
                        self.wifi_signal = None
                        # Reset to not detecting
                        self.detect = False

            self.consume(0, len(in0))

            """
            print("----------------------------------")
            print(f"{self.input_c = }, {len(in0) = }")
            self.input_c += 1
            
            if not self.detect:
                print(f"{self.detect = }")
                for tag in tags:
                    # Update to detected a wifi_start
                    # Convert from PMT to python string
                    key = pmt.to_python(tag.key)
                    if key == "wifi_start":
                        self.detect = True
                        # Get the start signal offset
                        offset = tag.offset
                        # Store the wifi signal to self.wifi_signal
                        self.wifi_signal = in0[offset:]

                        print(f"{len(in0) = } {offset = }, {len(self.wifi_signal) = }")
                # consume all the input
                self.consume(0, len(in0))

            elif self.wifi_signal is not None:
                # Already detected in the past.
                # Concatenate self.wifi_signal
                self.wifi_signal = np.concatenate((self.wifi_signal, in0))
                self.d_msg(f"{self.wifi_signal.shape = }, {len(self.wifi_signal) = }")
                
                offset = -1

                for tag in tags:
                    key = pmt.to_python(tag.key)
                    offset = tag.offset
                    print(f"{key = }, {len(in0) = }, {offset = }")

                if len(self.wifi_signal) >= self.max_sample:
                    num_last_sample = len(self.wifi_signal) - self.max_sample
                    # The length is longer than the wifi signal.
                    # Return the cut-off sample array.
                    # This ttl_sample should be output to the database
                    self.ttl_sample = self.wifi_signal[:self.max_sample]
                    self.d_msg(f"Complete packet with sample size: {self.ttl_sample.shape}")
                    print(f"save to db with sample: {len(self.ttl_sample) = }, {len(self.wifi_signal) = }")
                    self.save_to_db(self.ttl_sample)
                    # Erase the received packet
                    self.ttl_sample = None

                    # ---- Resetting
                    # Reset the detect flag
                    self.detect = False
                    # Clear the wifi_signal buffer
                    self.wifi_signal = None

                    if offset >= 0:
                        self.detect = True
                        self.wifi_signal = in0[offset:]
                        print(f"Acutally detect a concurrent packet. consume {len(in0)}")
                        print(f"{len(self.wifi_signal) = }")
                        self.consume(0, len(in0))
                    else:
                        self.consume(0, num_last_sample)
                        print(f"consume: {num_last_sample}")
                    pass
                else:
                    # It is not exceeding the max sample yet.
                    # consume all the input
                    print("Not exceeding. consume all and append self.wifi_signal")
                    print(f"{len(self.wifi_signal) = }")
                    self.consume(0, len(in0))
                # # Value can be several things, it depends what PMT type it was.
                # value = pmt.to_python(tag.value)
            else:
                print(f"{self.detect = }, self.wifi_signal is {self.wifi_signal}")
                self.consume(0, len(in0))
            """

        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            self.d_msg(f'Exception: {exp}. At line {e_tb.tb_lineno}')

        return False

