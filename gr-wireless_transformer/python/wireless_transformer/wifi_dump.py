#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 gr-wireless_transformer author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

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

        print(f"{in0.shape = }")

        return False
