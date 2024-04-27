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

FIND_RAISING_EDGE = 0
FIND_FALLING_EDGE = 1

RAISING_EDGE = 1
FALLING_EDGE = -1

class packet_saving(gr.sync_block):
    """
    docstring for block packet_saving
    """
    def __init__(self, 
                save_folder, 
                save_filename, 
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
        self.set_save_filename(save_filename)
        self.set_save_folder(save_folder)
        self.set_threshold(threshold)
        self.set_num_save_pkt(num_save_pkt)
        self.set_record(record)
        self.MIN_PKT_SIZE = 328
        self.PKT_LEN = 128

        self.init = True
        self.ttl_sample = 0

        self.update_save_filename()

        self.init_pkt_record()

    def d_msg(self, msg):
        if self.debug:
            print(msg)

    def reset_parameters(self, hard_reset_record=None):
        print("Resetting all the parameters...")
        if hard_reset_record is not None and not self.debug:
            print(f"Hard reset record to: {hard_reset_record}")
            self.set_record(hard_reset_record)

        self.ttl_packets = None
        self.init_pkt_record()
        print("Resetting Done.")

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
                self.reset_parameters()
            print(f"Setting {self.record: }")
        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            print(f'Exception: {exp}. At line {e_tb.tb_lineno}')

    def set_num_save_pkt(self, num_save_pkt):
        self.num_save_pkt = num_save_pkt

    def set_debug(self, debug):
        self.debug = debug
        print(f"Setting self.debug: {self.debug}")

    def set_save_folder(self, save_folder):
        self.save_folder = save_folder
        if not os.path.exists(self.save_folder):
            print(f"Directory {self.save_folder} does not exist. Create one.")
            os.makedirs(self.save_folder)
        self.update_save_filename()

    def set_save_filename(self, save_filename):
        self.save_filename = save_filename
        self.update_save_filename()

    def set_threshold(self, threshold):
        self.threshold = threshold
        print(f"Setting self.threshold: {self.threshold}")

    def update_save_filename(self):
        if self.init:
            self.save_full_filename = f"{self.save_folder}{self.save_filename}"
            print(f"Update to save to {self.save_full_filename}")
            self.reset_parameters()

    # ----------------------------------------------
    def where_over_threhsold(self, ary):
        return np.array([1 if x > self.threshold else 0 for x in ary])

    def get_moving_avg(self, ary):
        return ary.real

    def get_edges(self, above_list, i, edge=1):
        # Get raising edge and falling edge for the moving average curve
        # edge=1    : Find raising edge
        # edge=-1   : Find falling edge
        ret_edge = np.where(above_list[1:] - above_list[:-1] == edge)[0]
        if len(ret_edge) == 0:
            return None

        ret = np.where(ret_edge > i)[0][0]
        return ret

    def init_pkt_record(self):
        self.rgtr_pkt_i = 0
        self.pkt_s = 0
        self.state = FIND_RAISING_EDGE
        self.cur_pkt = None
        self.stage = 0
        pass

    def save_to_ttl_packet(self):
        # Save to registered array
        self.d_msg(f"Save to collected packets. len: {len(self.cur_pkt)}")

        trim_pkt = self.cur_pkt[200:]

        print(f"({trim_pkt.shape = })")
        for i in range(len(trim_pkt)):
            print(trim_pkt[i], end=', ')
        print('\n --------------')

        trim_num = int(trim_pkt.shape[0]/self.PKT_LEN)

        self.d_msg(f"Shape after trim: {trim_pkt.shape}, Total: {trim_num} new sample")
        ttl_trim_pkt = trim_pkt[:trim_num*self.PKT_LEN]
        ttl_trim_pkt_set = ttl_trim_pkt.reshape((trim_num, self.PKT_LEN))
        self.d_msg(f"{ttl_trim_pkt_set.shape = }")
        if self.ttl_packets is None:
            self.ttl_packets = ttl_trim_pkt_set
        else:
            self.ttl_packets = np.concatenate((self.ttl_packets, ttl_trim_pkt_set), axis=0)

        if self.ttl_packets.shape[0] >= self.num_save_pkt:
            print("Have enough samples! Save to file")
            
            self.ttl_packets = self.ttl_packets[:self.num_save_pkt]
            self.d_msg(f"{self.ttl_packets.shape = }")
            if self.record:
                if os.path.exists(self.save_full_filename):
                    print("Already exists. Do not overwrite")
                    # self.ttl_packets.tofile(self.save_full_filename)
                else:
                    print(f"Saving to file: {self.save_full_filename}")
                    print(f"Save array shape: {self.ttl_packets.shape}")

                    self.ttl_packets.tofile(self.save_full_filename)

            print("Resetting everything.")
            self.reset_parameters(hard_reset_record=False)
        else:
            self.d_msg(f"Current record samples: {self.ttl_packets.shape[0]}")

    # ----------------------------------------------
    def work(self, input_items, output_items):
        try:
            in0 = input_items[0]
            in1 = input_items[1]

            if not self.record:
                self.consume_each(len(in0))
                return False

            mov_avg = in1.real
            is_above_threshold = self.where_over_threhsold(mov_avg)
            self.d_msg("-"*50)

            self.pkt_s = 0

            for i, is_above in enumerate(is_above_threshold):
                if self.state == FIND_RAISING_EDGE:
                    if is_above == 1:
                        # FIND_RAISING_EDGE
                        self.pkt_s = i
                        self.state = FIND_FALLING_EDGE
                        if self.stage != 1:
                            self.d_msg(f"[{self.ttl_sample+i}] Found the start of a packet")
                            self.stage = 1
                    else:
                        if self.state != 0:
                            self.d_msg(f"[{self.ttl_sample+i}] Nothing found")
                            self.stage = 0
                elif self.state == FIND_FALLING_EDGE:
                    if is_above == 0:
                        # FIND_FALLING_EDGE
                        if i - self.pkt_s + self.rgtr_pkt_i > self.MIN_PKT_SIZE:
                            # It is long enough
                            self.d_msg(f"[{self.ttl_sample+i}] Found the end of a packet")
                            self.pkt_e = i
                            if self.cur_pkt is None:
                                if self.stage != 2:
                                    self.d_msg(f"[{self.ttl_sample+i}] A whole new packet.")
                                    self.stage = 2
                                self.cur_pkt = in0[self.pkt_s:self.pkt_e]
                            else:
                                if self.stage != 3:
                                    self.d_msg(f"[{self.ttl_sample+i}] Concatenate to a old sub-packet.")
                                    self.stage = 3
                                self.rgtr_pkt_i += len(in0[:self.pkt_e])
                                self.cur_pkt = np.concatenate((self.cur_pkt, in0[:self.pkt_e]))
                            
                            self.save_to_ttl_packet()

                            # Reset
                            self.d_msg("Reset the mode")
                            self.init_pkt_record()
                        elif i == len(is_above_threshold) - 1:
                            # Not long enough and meet the end of input
                            if self.stage != 4:
                                self.d_msg(f"[{i}] Nothing found as the end of a packet. Concatenate whole input.")
                                self.stage = 4

                            if self.cur_pkt is None:
                                self.cur_pkt = in0[self.pkt_s:]
                            else:
                                self.rgtr_pkt_i += len(in0[self.pkt_s:])
                                self.cur_pkt = np.concatenate((self.cur_pkt, in0[self.pkt_s:]))
                        else:
                            if self.stage != 5:
                                self.d_msg(f"[{i}] Should NOT be here. [1]")
                                self.stage = 5
                    else:
                        if i == len(is_above_threshold) - 1:
                            self.d_msg(f"[{self.ttl_sample+i}] End of Input. Still a raising wave.")
                            if self.cur_pkt is None:
                                self.cur_pkt = in0[self.pkt_s:]
                                self.d_msg(f"[{self.ttl_sample+i}] Temperary record a new packet.")
                            else:
                                self.rgtr_pkt_i += len(in0)
                                self.cur_pkt = np.concatenate((self.cur_pkt, in0))
                                self.d_msg(f"[{self.ttl_sample+i}] Concatenate to the eamperary packet.")
                    pass

            self.ttl_sample += len(in1)
            # print(f"{self.ttl_sample = }")
            self.consume_each(len(in0))
        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            print(f'Exception: {exp}. At line {e_tb.tb_lineno}')
        return False