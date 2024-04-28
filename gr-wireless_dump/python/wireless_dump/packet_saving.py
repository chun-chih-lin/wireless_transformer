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
                save_prefix, 
                save_mod,
                tx_pwr,
                distance=1, 
                samp_rate=5e6,
                carrier_freq=2360e6,
                interference=0, 
                threshold=0.005, 
                num_save_pkt=20_000, 
                debug=False, 
                record=False, 
                overwrite=False):
        gr.sync_block.__init__(self,
            name="packet_saving",
            in_sig=[np.complex64, np.complex64],
            out_sig=None)

        self.init = False

        self.set_debug(debug)
        # self.set_save_filename(save_filename)

        self.set_save_prefix(save_prefix)
        self.set_save_mod(save_mod)
        self.set_distance(distance)
        self.set_tx_pwr(tx_pwr)
        self.set_carrier_freq(carrier_freq)
        self.set_interference(interference)
        self.set_samp_rate(samp_rate)

        self.set_save_folder(save_folder)
        self.set_threshold(threshold)
        self.set_num_save_pkt(num_save_pkt)
        self.set_record(record)
        self.set_overwrite(overwrite)
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
        print("==== Resetting all the parameters...")
        if hard_reset_record is not None and not self.debug:
            print(f"Hard reset record to: {hard_reset_record}")
            self.set_record(hard_reset_record)

        self.progress = 0
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
            print(f"Setting Record to {self.record: }")
        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            print(f'Exception: {exp}. At line {e_tb.tb_lineno}')

    def set_num_save_pkt(self, num_save_pkt):
        self.num_save_pkt = num_save_pkt

    def set_debug(self, debug):
        self.debug = debug
        print(f"Setting self.debug: {self.debug}")

    def set_overwrite(self, overwrite):
        self.overwrite = overwrite
        print(f"Setting self.overwrite: {self.overwrite}")

    def set_save_folder(self, save_folder):
        self.save_folder = save_folder
        if not os.path.exists(self.save_folder):
            print(f"Directory {self.save_folder} does not exist. Create one.")
            os.makedirs(self.save_folder)
        self.update_save_filename()

    # def set_save_filename(self, save_filename):
    #     self.save_filename = save_filename
    #     self.update_save_filename()

    # ----------------------------------------
    def set_save_prefix(self, save_prefix):
        self.save_prefix = save_prefix
        print(f"Updating save_prefix to {self.save_prefix}")
        self.update_save_filename()

    def set_save_mod(self, save_mod):
        self.save_mod = save_mod
        print(f"Updating save_mod to {self.save_mod}")
        self.update_save_filename()

    def set_tx_pwr(self, tx_pwr):
        self.tx_pwr = tx_pwr
        print(f"Updating tx_pwr to {self.tx_pwr}")
        self.update_save_filename()

    def set_distance(self, distance):
        self.distance = distance
        print(f"Updating distance to {self.distance}")
        self.update_save_filename()

    def set_samp_rate(self, samp_rate):
        self.samp_rate = int(samp_rate/1e6)
        print(f"Updating samp_rate to {self.samp_rate}")
        self.update_save_filename()

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = int(carrier_freq/1e6)
        print(f"Updating carrier_freq to {self.carrier_freq}")
        self.update_save_filename()

    def set_interference(self, interference):
        self.interference = interference
        print(f"Updating interference to {self.interference}")
        self.update_save_filename()

    # ----------------------------------------
    def set_threshold(self, threshold):
        self.threshold = threshold
        print(f"Setting self.threshold: {self.threshold}")

    def update_save_filename(self):
        if self.init:
            self.save_filename = f"{self.save_prefix}_{self.save_mod}_TP{self.tx_pwr}_D{self.distance}_SR{self.samp_rate}_CF{self.carrier_freq}_I{self.interference}.dat"
            self.save_full_filename = f"{self.save_folder}{self.save_filename}"
            print(f"==== Update to save to {self.save_full_filename}")
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

        # print(f"({trim_pkt.shape = })")
        # for i in range(len(trim_pkt)):
        #     print(trim_pkt[i], end=', ')
        # print('\n --------------')

        trim_num = int(trim_pkt.shape[0]/self.PKT_LEN)

        self.d_msg(f"Shape after trim: {trim_pkt.shape}, Total: {trim_num} new sample")
        ttl_trim_pkt = trim_pkt[:trim_num*self.PKT_LEN]
        ttl_trim_pkt_set = ttl_trim_pkt.reshape((trim_num, self.PKT_LEN))
        self.d_msg(f"{ttl_trim_pkt_set.shape = }")
        if self.ttl_packets is None:
            self.ttl_packets = ttl_trim_pkt_set
        else:
            self.ttl_packets = np.concatenate((self.ttl_packets, ttl_trim_pkt_set), axis=0)


        current_percentage = int(self.ttl_packets.shape[0]/self.num_save_pkt*10)
        if current_percentage == self.progress + 1:
            print(f"Progress: {self.ttl_packets.shape[0]}/{self.num_save_pkt} = {current_percentage*10}%...")
            self.progress += 1

        if self.ttl_packets.shape[0] >= self.num_save_pkt:
            print(f"Have enough samples! Save to file: {self.save_full_filename}")
            
            self.ttl_packets = self.ttl_packets[:self.num_save_pkt]
            self.d_msg(f"{self.ttl_packets.shape = }")
            if self.record:
                if os.path.exists(self.save_full_filename) and not self.overwrite:
                    print("Already exists. Do not overwrite")
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
                    # ----------------------------------------
                    if is_above == 1: # It is a high
                        if i == len(is_above_threshold) - 1: 
                            # Meeting the end of input, and it is still high
                            sub_wf = in0[self.pkt_s:]
                            if self.cur_pkt is None:
                                self.cur_pkt = sub_wf
                                self.d_msg(f"[{self.ttl_sample+i}] Metting the end of input. Temperary record a new packet.")
                            else:
                                self.cur_pkt = np.concatenate((self.cur_pkt, sub_wf))
                                self.d_msg(f"[{self.ttl_sample+i}] Metting the end of input. Concatenate to the eamperary packet.")
                            self.rgtr_pkt_i += len(sub_wf)
                        else:
                            # It is still high and in the middle of the input
                            # Do nothing.
                            pass

                    else: # It seems to be an end of packet.
                        if i - self.pkt_s + self.rgtr_pkt_i < self.MIN_PKT_SIZE: 
                            # It is not long enough
                            if i == len(is_above_threshold) - 1: 
                                # It is not long enough but meet the end of input
                                sub_wf = in0[self.pkt_s:]
                                if self.cur_pkt is None:
                                    self.cur_pkt = sub_wf
                                    self.d_msg(f"[{self.ttl_sample+i}] Metting the end of input. Temperary record a new packet.")
                                else:
                                    self.cur_pkt = np.concatenate((self.cur_pkt, sub_wf))
                                    self.d_msg(f"[{self.ttl_sample+i}] Metting the end of input. Concatenate to the eamperary packet.")
                                self.rgtr_pkt_i += len(sub_wf)
                            else:
                                # It is not long enough and in the middle of the input.
                                # Do nothing.
                                pass
                        elif i - self.pkt_s + self.rgtr_pkt_i > self.MIN_PKT_SIZE: 
                            # It is long enough
                            sub_wf = in0[self.pkt_s:i]

                            self.d_msg(f"[{self.ttl_sample+i}] Found the end of a packet")
                            if self.cur_pkt is None:
                                if self.stage != 2:
                                    self.d_msg(f"[{self.ttl_sample+i}] A whole new packet. {len(sub_wf)}")
                                    self.stage = 2

                                self.cur_pkt = sub_wf
                            else:
                                if self.stage != 3:
                                    self.d_msg(f"[{self.ttl_sample+i}] Concatenate to a old sub-packet. {len(self.cur_pkt)} + {len(sub_wf)}]")
                                    self.stage = 3

                                self.cur_pkt = np.concatenate((self.cur_pkt, sub_wf))
                            self.rgtr_pkt_i += len(sub_wf)

                            self.save_to_ttl_packet()

                            # Reset
                            self.d_msg("Reset the mode")
                            self.init_pkt_record()
                    #     # -------------------------
                    #     elif i == len(is_above_threshold) - 1: # Not long enough and meet the end of input
                    #         sub_wf = in0[self.pkt_s:]
                    #         if self.cur_pkt is None:
                    #             if self.stage != 4:
                    #                 self.d_msg(f"[{i}] Nothing found as the end of a packet. Create a new sub-packet. {len(self.cur_pkt)} + {len(sub_wf)}")
                    #                 self.stage = 4    
                    #             self.cur_pkt = sub_wf
                    #         else:
                    #             if self.stage != 5:
                    #                 self.d_msg(f"[{i}] Nothing found as the end of a packet. Concatenate whole input. {len(self.cur_pkt)} + {len(sub_wf)}")
                    #                 self.stage = 5
                    #             self.cur_pkt = np.concatenate((self.cur_pkt, sub_wf))
                    #         self.rgtr_pkt_i += len(sub_wf)
                    #     else:
                    #         if self.stage != 6:
                    #             self.d_msg(f"[{i}] Should NOT be here. [1]")
                    #             self.stage = 6
                    # # ----------------------------------------
                    # else: # still is a high curve
                    #     if i == len(is_above_threshold) - 1: # Meet the end of the input
                    #         sub_wf = in0[self.pkt_s:]
                    #         self.d_msg(f"[{self.ttl_sample+i}] End of Input. Still a raising wave.")
                    #         if self.cur_pkt is None:
                    #             self.cur_pkt = sub_wf
                    #             self.d_msg(f"[{self.ttl_sample+i}] Temperary record a new packet.")
                    #         else:
                    #             self.cur_pkt = np.concatenate((self.cur_pkt, sub_wf))
                    #             self.d_msg(f"[{self.ttl_sample+i}] Concatenate to the eamperary packet.")
                    #         self.rgtr_pkt_i += len(sub_wf)
                    pass

            self.ttl_sample += len(in1)
            # print(f"{self.ttl_sample = }")
            self.consume_each(len(in0))
        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            print(f'Exception: {exp}. At line {e_tb.tb_lineno}')
        return False