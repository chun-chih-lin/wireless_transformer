#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 gr-wireless_dump author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr
import pmt, json, sys, os

class packet_saving(gr.sync_block):
    """
    docstring for block packet_saving
    """
    def __init__(self, 
                mod, 
                tx_pwr, 
                save_folder, 
                save_prefix, 
                carrier_freq=2360e6, 
                samp_rate=5e6, 
                threshold=0.005, 
                num_save_pkt=20_000, 
                debug=False, 
                record=False):
        gr.sync_block.__init__(self,
            name="packet_saving",
            in_sig=[np.complex64, np.complex64],
            out_sig=None)
        self.init = False
        self.set_debug(debug)
        self.set_mod(mod)
        self.set_tx_pwr(tx_pwr)

        self.set_save_prefix(save_prefix)
        self.set_save_folder(save_folder)
        
        self.set_carrier_freq(carrier_freq)
        self.set_samp_rate(samp_rate)
        self.set_threshold(threshold)
        self.set_num_save_pkt(num_save_pkt)

        self.set_record(record)

        self.init = True
        self.update_save_filename()


    # ----------------------------------------------
    # Callback functions
    def set_record(self, record):
        try:
            if int(record) == 1:
                self.record = True
                # reset the recorded number of packets
                self.recorded_pkt = 0
            else:
                self.record = False
            print(f"Setting {self.record: }")
        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            print(f'Exception: {exp}. At line {e_tb.tb_lineno}')

    def set_num_save_pkt(self, num_save_pkt):
        self.num_save_pkt = num_save_pkt

    def set_debug(self, debug):
        self.debug = debug
        print(f"Setting self.debug: {self.debug}")

    def set_mod(self, mod):
        self.mod = mod
        self.update_save_filename()

    def set_tx_pwr(self, tx_pwr):
        self.tx_pwr = tx_pwr
        self.update_save_filename()

    def set_save_folder(self, save_folder):
        self.save_folder = f"{save_folder}{self.save_prefix}/"
        if not os.path.exists(self.save_folder):
            print(f"Directory {self.save_folder} does not exist. Create one.")
            os.makedirs(self.save_folder)
        self.update_save_filename()

    def set_save_prefix(self, save_prefix):
        self.save_prefix = save_prefix
        self.update_save_filename()

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.carrier_freq_in_MHz = int(self.carrier_freq/1e6)
        self.update_save_filename()

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.samp_rate_in_MHz = int(self.samp_rate/1e6)
        self.update_save_filename()

    def set_threshold(self, threshold):
        self.threshold = threshold

    def update_save_filename(self):
        if self.init:
            self.save_filename = f"{self.save_prefix}_{self.mod}_{self.tx_pwr}_{self.samp_rate_in_MHz}_{self.carrier_freq_in_MHz}.dat"
            self.save_full_filename = f"{self.save_folder}{self.save_filename}"
            print(f"Update to save to {self.save_full_filename}")

    # ----------------------------------------------
    def work(self, input_items, output_items):
        try:

            in0 = input_items[0]
            in1 = input_items[1]

            moving_avg_ret = in1.real
            # thresold = in1.imag

            above_threshold = np.where(moving_avg_ret > self.threshold)


            self.consume(0, len(in0))
            self.consume(1, len(in1))

        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            print(f'Exception: {exp}. At line {e_tb.tb_lineno}')
        return False
