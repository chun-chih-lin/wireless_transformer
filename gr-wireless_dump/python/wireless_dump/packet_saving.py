#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 gr-wireless_dump author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

class packet_saving(gr.sync_block):
    """
    docstring for block packet_saving
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="packet_saving",
            in_sig=[<+numpy.float32+>, ],
            out_sig=None)


    def work(self, input_items, output_items):
        in0 = input_items[0]
        # <+signal processing here+>
        return len(input_items[0])
