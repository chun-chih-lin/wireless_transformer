#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 gr-wireless_dump author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

class capture_signal_on_tx(gr.sync_block):
    """
    docstring for block capture_signal_on_tx
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="capture_signal_on_tx",
            in_sig=[<+numpy.float32+>, ],
            out_sig=None)


    def work(self, input_items, output_items):
        in0 = input_items[0]
        # <+signal processing here+>
        return len(input_items[0])
