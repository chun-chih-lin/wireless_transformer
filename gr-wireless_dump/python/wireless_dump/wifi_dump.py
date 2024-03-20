#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 gr-wireless_dump author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
import pmt, json

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

class wifi_dump(gr.sync_block):
    """
    docstring for block wifi_dump
    """
    def __init__(self, mod, pdu_len):
        gr.sync_block.__init__(self,
            name="wifi_dump",
            in_sig=[np.complex64],
            out_sig=None)
        self.count = 0
        self.wifi_signal = None
        self.detect = False
        self.pdu_len = None
        self.set_modulation(mod)
        self.set_pdu_len(pdu_len)
        
    def set_modulation(self, mod):
        self.mod = mod
        if self.pdu_len is not None:
            self.update_ttl_sample()
        
    def set_pdu_len(self, pdu_len):
        self.pdu_len = pdu_len
        self.update_ttl_sample()

    def update_ttl_sample(self):
        print("Updating wifi signal length...")
        print(f"{self.pdu_len = }, {self.mod = }")

        

        # header size is 24 bytes
        # pdu size id pdu_len bytes
        # FCS size is 4 bytes

        

        max_sample = 5000
        self.max_sample = max_sample

    def work(self, input_items, output_items):
        in0 = input_items[0]
        tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        
        if not self.detect:
            for tag in tags:
                # Update to detected a wifi_start
                self.detect = True

                # Get the start signal offset
                offset = tag.offset

                # Store the wifi signal to self.wifi_signal
                self.wifi_signal = in0[offset:]
        elif self.wifi_signal is not None:
            if len(self.wifi_signal) >= self.max_sample:
                # The length is longer than the wifi signal.
                # Return the whole sample array.
                self.ttl_sample = self.wifi_signal
                # Reset the detect flag
                #self.detect = False
                # Clear the wifi_signal buffer
                self.wifi_signal = None
                self.detect = False
                pass
            else:
                # Already detected in the past.
                # Concatenate self.wifi_signal
                self.wifi_signal = np.concatenate((self.wifi_signal, in0))
                # print(f"{self.wifi_signal = }, {len(self.wifi_signal) = }")

            # # Convert from PMT to python string
            # key = pmt.to_python(tag.key)
            # # Value can be several things, it depends what PMT type it was.
            # value = pmt.to_python(tag.value)

        return False
