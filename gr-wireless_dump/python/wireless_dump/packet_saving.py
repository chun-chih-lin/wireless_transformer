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
        self.MIN_PKT_SIZE = 100

        self.init = True

        self.update_save_filename()

        self.init_pkt_record()

    def d_msg(self, msg):
        if self.debug:
            print(msg)

    def reset_parameters(self):
        print("Resetting all the parameters...")
        self.ttl_packets = None

        self.cur_packet = None
        self.pkt_start = None
        self.pkt_end = None

        self.state = FIND_RAISING_EDGE
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

    # ----------------------------------------------
    def work(self, input_items, output_items):
        try:
            in0 = input_items[0]
            in1 = input_items[1]

            mov_avg = in1.real
            
            is_above_threshold = self.where_over_threhsold(mov_avg)

            for i, is_above in enumerate(is_above_threshold):
                if self.state == FIND_RAISING_EDGE:
                    if is_above == 1:
                        # FIND_RAISING_EDGE
                        self.pkt_s = i
                        self.state = FIND_FALLING_EDGE
                        if self.stage != 0:
                            print(f"[{i}] Found the start of a packet")
                            self.stage = 1
                    else:
                        
                        if self.stage != 1:
                            print(f"[{i}] Nothing found")
                            self.stage = 0
                elif self.state == FIND_FALLING_EDGE:
                    if is_above == 0:
                        # FIND_FALLING_EDGE
                        if i - self.pkt_s + self.rgtr_pkt_i > self.MIN_PKT_SIZE:
                            print("Found the end of a packet")
                            self.pkt_e = i
                            if self.cur_pkt is None:
                                if self.stage != 2:
                                    print(f"[{i}] A whole new packet.")
                                    self.stage = 2
                                self.cur_pkt = in0[self.pkt_s:self.pkt_e]
                            else:
                                if self.stage != 3:
                                    print(f"[{i}] Concatenate to a old sub-packet.")
                                    self.stage = 3
                                self.cur_pkt = np.concatenate(self.cur_pkt, in0[:self.pkt_e])
                            
                            # Save to registered array
                            print("Save to collected packets")
                            # Reset
                            print("Reset the mode")
                            self.init_pkt_record()
                        elif i == len(in0):
                            if self.stage != 4:
                                print(f"[{i}] Nothing found as the end of a packet. Concatenate whole input.")
                                self.stage = 4
                            self.cur_pkt = np.concatenate(self.cur_pkt, in0)
                        else:
                            if self.stage != 5:
                                print(f"[{i}] Should NOT be here. [1]")
                                self.stage = 5
                    else:
                        if self.stage != 6:
                            print(f"[{i}] Is still a raising wave.")
                            self.stage = 6
                    pass

            self.consume_each(len(in0))



            """

            i = 0
            while i < len(in0):
                print("-"*50)
                print(f"{len(in0) = }, {len(in1) = }")

                current_raw_wave = in0
                current_moving_avg_wave = in1

                moving_avg_ret = self.get_moving_avg(in1)
                above_list = self.where_over_threhsold(moving_avg_ret)

                if self.state == FIND_RAISING_EDGE:
                    print(f"Trying to find a new packet.")
                    # Find a new packet
                    if len(np.where(above_list > 0)[0]) == 0:
                        # Nothing is greater than the threshold
                        i += len(in0)
                        self.consume_each(len(in0))
                        print(f"Nothing is greater than the threshold. consume({len(in0)})")
                        continue

                    print(f"First greater than threshold: {np.where(above_list == 1)[0][0]}")
                    r_edge_idx = self.get_edges(above_list, i, edge=RAISING_EDGE)

                    if r_edge_idx is None:
                        # Raising Edge is not detected
                        i += len(in0)
                        self.consume_each(len(in0))
                        print(f"Raising Edge is not detected. consume({len(in0)})")
                        continue

                    self.pkt_start = r_edge_idx
                    print(f"Find the Raising edge: {self.pkt_start}. Go to State 2.")
                    self.state = FIND_FALLING_EDGE

                else:
                    # Find the end of the packet
                    f_edge_idx = self.get_edges(above_list, i, edge=FALLING_EDGE)

                    if f_edge_idx is None:
                        # Do not find any falling edge.
                        if self.cur_packet is None:
                            self.cur_packet = in0[self.pkt_start:]
                            self.pkt_start = 0
                        else:
                            self.cur_packet = np.concatenate((self.cur_packet, in0))

                        i += len(in0)
                        self.consume_each(len(in0))
                        continue

                    # Find at least one falling edge.
                    while f_edge_idx - self.pkt_start <= self.MIN_PKT_SIZE:
                        print(f"{f_edge_idx} - {self.pkt_start} <= {self.MIN_PKT_SIZE}. Search for the next.")
                        f_edge_idx = self.get_edges(above_list, i+f_edge_idx, edge=FALLING_EDGE)
                        pass

                    if self.pkt_end is not None:
                        # get a complete packet
                        rest_pkt = in0[self.pkt_start:self.pkt_end]
                        if self.cur_packet is None:
                            self.cur_packet = rest_pkt
                        else:
                            self.cur_packet = np.concatenate((self.cur_packet, rest_pkt))
                        
                        # Expand the simension of the complete packet.
                        cur_packet = np.expand_dims(self.cur_packet, axis=0)

                        # Save to total packets
                        if self.ttl_packets is None:
                            self.ttl_packets = cur_packet
                        else:
                            self.ttl_packets = np.concatenate((self.ttl_packets, cur_packet), axis=0)
                        # Check if the number of packet is enough
                        if self.ttl_packets.shape[0] >= self.num_save_pkt:
                            print(f"Saving packet into file {self.save_full_filename}")
                            self.ttl_packets.tofile(self.save_full_filename)
                            print(f"Reset the ttl_packet to None.")
                            self.ttl_packets = None

                        # resetting parameters
                        self.cur_packet = None
                        self.pkt_start = None
                        self.pkt_end = None
                        self.state = FIND_RAISING_EDGE

                        # self.consume_each(len(self.cur_packet))
                        i += len(self.cur_packet)
                        self.consume(0, len(self.cur_packet))
                        self.consume(1, len(self.cur_packet))

                    else:
                        # non of the edge works
                        self.cur_packet = np.concatenate((self.cur_packet, in0))
                        # self.consume_each(len(in0))
                        i += len(in0)
                        self.consume(0, len(in0))
                        self.consume(1, len(in1))
            print("Out-of-while")
            """

        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            print(f'Exception: {exp}. At line {e_tb.tb_lineno}')
        return False
