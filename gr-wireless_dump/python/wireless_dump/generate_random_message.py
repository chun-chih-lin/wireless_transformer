#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 gr-wireless_dump author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

class generate_random_message(gr.sync_block):
    """
    docstring for block generate_random_message
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="generate_random_message",
            in_sig=None,
            out_sig=[<+numpy.float32+>, ])


    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>
        out[:] = whatever
        return len(output_items[0])
