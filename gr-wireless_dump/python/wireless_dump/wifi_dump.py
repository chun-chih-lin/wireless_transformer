#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 gr-wireless_dump author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
import pmt

class wifi_dump(gr.sync_block):
    """
    docstring for block wifi_dump
    """
    def __init__(self, mod, pkt_len):
        gr.sync_block.__init__(self,
            name="wifi_dump",
            in_sig=[np.complex64],
            out_sig=None)
        self.count = 0
        self.wifi_signal = None
        self.detect = False
        self.pkt_len = None
        self.set_modulation(mod)
        self.set_pkt_len(pkt_len)
        
    def set_modulation(self, mod):
        self.mod = mod
        if self.pkt_len is not None:
            self.calculate_wifi_len()
        
    def set_pkt_len(self, pkt_len):
        self.pkt_len = pkt_len
        self.calculate_wifi_len()

    def calculate_wifi_len(self):
        print("Updating wifi signal length...")
        print(f"{self.pkt_len = }, {self.mod = }")

        wifi_len = 5000
        self.wifi_len = wifi_len

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
        else:
            if len(self.wifi_signal) >= self.wifi_len:
                # The length is longer than the wifi signal.
                # Do not do anything.
                pass
            else:
                # Already detected in the past.
                # Concatenate self.wifi_signal
                self.wifi_signal = np.concatenate((self.wifi_signal, in0))
                print(f"{self.wifi_signal = }, {len(self.wifi_signal) = }")

            # # Convert from PMT to python string
            # key = pmt.to_python(tag.key)
            # # Value can be several things, it depends what PMT type it was.
            # value = pmt.to_python(tag.value)

        return False
