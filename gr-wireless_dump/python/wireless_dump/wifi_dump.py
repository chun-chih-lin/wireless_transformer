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
    def __init__(self):
        gr.sync_block.__init__(self,
            name="wifi_dump",
            in_sig=[np.complex64],
            out_sig=None)


    def work(self, input_items, output_items):
        in0 = input_items[0]
        tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        for tag in tags:
            # Convert from PMT to python string
            key = pmt.to_python(tag.key)

            # Value can be several things, it depends what PMT type it was.
            value = pmt.to_python(tag.value)

            print(f"{key = }")
            print(f"{value = }")
        return False
