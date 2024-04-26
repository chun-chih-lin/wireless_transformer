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

    def get_edges(self, above_list, edge=1):
        # Get raising edge and falling edge for the moving average curve
        # edge=1    : Find raising edge
        # edge=-1   : Find falling edge
        ret_edge = np.where(above_list[1:] - above_list[:-1] == edge)[0]
        return ret_edge

    # ----------------------------------------------
    def work(self, input_items, output_items):
        try:
            in0 = input_items[0]
            in1 = input_items[1]

            i = 0
            while len(in0) > 0 and len(in1) > 0:
                if self.state == FIND_RAISING_EDGE:
                    # Find a new packet
                    moving_avg_ret = self.get_moving_avg(in1)
                    above_list = self.where_over_threhsold(moving_avg_ret)

                    if np.isscalar(above_list):
                        # Nothing is greater than the threshold
                        self.consume_each([len(in0), len(in1)])
                        pass

                    r_edge = self.get_edges(above_list, edge=RAISING_EDGE)
                    self.pkt_start = r_edge[0]
                    self.state = FIND_FALLING_EDGE

                    self.consume_each([self.pkt_start, self.pkt_start])
                else:
                    # Find the end of the packet
                    f_edge = self.get_edges(above_list, edge=FALLING_EDGE)

                    if np.isscalar(f_edge):
                        # Do not find any falling edge.
                        if self.cur_packet is None:
                            self.cur_packet = in0
                        else:
                            self.cur_packet = np.concatenate((self.cur_packet, in0))

                        self.consume_each([len(in0), len(in0)])
                        continue

                    # Find at least one falling edge.
                    k = 0
                    while k < len(f_edge):
                        if f_edge - self.r_edge >= self.MIN_PKT_SIZE:
                            self.pkt_end = f_edge[k]        
                            break
                        k += 1
                        pass

                    if self.pkt_end is not None:
                        # get a complete packet
                        self.cur_packet = in0[:self.pkt_end]
                        
                        cur_packet = np.expand_dims(self.cur_packet, axis=0)

                        if self.ttl_packets is None:
                            self.ttl_packets = cur_packet
                        else:
                            self.ttl_packets = np.concatenate((self.ttl_packets, cur_packet), axis=0)

                        if self.ttl_packets.shape[0] >= self.num_save_pkt:
                            print(f"Saving packet into file {self.save_full_filename}")
                            self.ttl_packets.tofile(self.save_full_filename)
                            print(f"Reset the ttl_packet to None.")
                            self.ttl_packets = None

                        self.cur_packet = None
                        self.pkt_start = None
                        self.pkt_end = None
                        self.state = FIND_RAISING_EDGE

                        self.consume_each([len(self.cur_packet), len(self.cur_packet)])

                    else:
                        # non of the edge works
                        self.cur_packet = np.concatenate((self.cur_packet, in0))
                        self.consume_each([len(in0), len(in0)])


                # self.consume(0, len(in0))
                # self.consume(1, len(in1))

        except Exception as exp:
            e_type, e_obj, e_tb = sys.exc_info()
            print(f'Exception: {exp}. At line {e_tb.tb_lineno}')
        return False
