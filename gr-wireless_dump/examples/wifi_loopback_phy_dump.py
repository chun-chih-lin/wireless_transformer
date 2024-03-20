#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: root
# GNU Radio version: v3.10.9.2-5-gdd01ef52

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import blocks
import pmt
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import wireless_dump
from gnuradio.filter import pfb
import foo
import ieee802_11
import sip



class wifi_loopback_phy_dump(gr.top_block, Qt.QWidget):

    def __init__(self, sensitivity=0.56):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "wifi_loopback_phy_dump")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Parameters
        ##################################################
        self.sensitivity = sensitivity

        ##################################################
        # Variables
        ##################################################
        self.window_size = window_size = 48
        self.sync_length = sync_length = 320
        self.snr = snr = 15
        self.samp_rate = samp_rate = 20e6
        self.pdu_length = pdu_length = 10
        self.out_buf_size = out_buf_size = 96000
        self.max_symbols = max_symbols = int(5 + 1 + ((16 + 800 * 8 + 6) * 2) / 24)
        self.interval = interval = 2000
        self.header_formatter = header_formatter = ieee802_11.signal_field()
        self.freq = freq = 5890000000
        self.epsilon = epsilon = 0
        self.encoding = encoding = 0
        self.chan_est = chan_est = 0
        self.Debug = Debug = 0

        ##################################################
        # Blocks
        ##################################################

        self._snr_range = qtgui.Range(-15, 30, 0.1, 15, 200)
        self._snr_win = qtgui.RangeWidget(self._snr_range, self.set_snr, "'snr'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._snr_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._samp_rate_options = [5000000.0, 10000000.0, 20000000.0]
        # Create the labels list
        self._samp_rate_labels = ['5 MHz', '10 MHz', '20 MHz']
        # Create the combo box
        self._samp_rate_tool_bar = Qt.QToolBar(self)
        self._samp_rate_tool_bar.addWidget(Qt.QLabel("'samp_rate'" + ": "))
        self._samp_rate_combo_box = Qt.QComboBox()
        self._samp_rate_tool_bar.addWidget(self._samp_rate_combo_box)
        for _label in self._samp_rate_labels: self._samp_rate_combo_box.addItem(_label)
        self._samp_rate_callback = lambda i: Qt.QMetaObject.invokeMethod(self._samp_rate_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._samp_rate_options.index(i)))
        self._samp_rate_callback(self.samp_rate)
        self._samp_rate_combo_box.currentIndexChanged.connect(
            lambda i: self.set_samp_rate(self._samp_rate_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._samp_rate_tool_bar)
        self._pdu_length_range = qtgui.Range(0, 1500, 1, 10, 200)
        self._pdu_length_win = qtgui.RangeWidget(self._pdu_length_range, self.set_pdu_length, "'pdu_length'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._pdu_length_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._interval_range = qtgui.Range(10, 10000, 1, 2000, 200)
        self._interval_win = qtgui.RangeWidget(self._interval_range, self.set_interval, "'interval'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._interval_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._epsilon_range = qtgui.Range(-20e-6, 20e-6, 1e-6, 0, 200)
        self._epsilon_win = qtgui.RangeWidget(self._epsilon_range, self.set_epsilon, "'epsilon'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._epsilon_win, 3, 1, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._encoding_options = [0, 1, 2, 3, 4, 5, 6, 7]
        # Create the labels list
        self._encoding_labels = ['BPSK 1/2', 'BPSK 3/4', 'QPSK 1/2', 'QPSK 3/4', '16QAM 1/2', '16QAM 3/4', '64QAM 2/3', '64QAM 3/4']
        # Create the combo box
        self._encoding_tool_bar = Qt.QToolBar(self)
        self._encoding_tool_bar.addWidget(Qt.QLabel("'encoding'" + ": "))
        self._encoding_combo_box = Qt.QComboBox()
        self._encoding_tool_bar.addWidget(self._encoding_combo_box)
        for _label in self._encoding_labels: self._encoding_combo_box.addItem(_label)
        self._encoding_callback = lambda i: Qt.QMetaObject.invokeMethod(self._encoding_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._encoding_options.index(i)))
        self._encoding_callback(self.encoding)
        self._encoding_combo_box.currentIndexChanged.connect(
            lambda i: self.set_encoding(self._encoding_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._encoding_tool_bar, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._Debug_options = [0, 1]
        # Create the labels list
        self._Debug_labels = [False, True]
        # Create the combo box
        self._Debug_tool_bar = Qt.QToolBar(self)
        self._Debug_tool_bar.addWidget(Qt.QLabel("'Debug'" + ": "))
        self._Debug_combo_box = Qt.QComboBox()
        self._Debug_tool_bar.addWidget(self._Debug_combo_box)
        for _label in self._Debug_labels: self._Debug_combo_box.addItem(_label)
        self._Debug_callback = lambda i: Qt.QMetaObject.invokeMethod(self._Debug_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._Debug_options.index(i)))
        self._Debug_callback(self.Debug)
        self._Debug_combo_box.currentIndexChanged.connect(
            lambda i: self.set_Debug(self._Debug_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._Debug_tool_bar)
        self.wireless_dump_wifi_dump_0 = wireless_dump.wifi_dump(0, pdu_length, Debug)
        self.sync_short = ieee802_11.sync_short(sensitivity, 2, False, False)
        self.sync_long = ieee802_11.sync_long(sync_length, False, False)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
            (1+epsilon),
            taps=None,
            flt_size=32,
            atten=100)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)
        self.ieee802_11_mapper_0 = ieee802_11.mapper(encoding, False)
        self.ieee802_11_mac_0_0 = ieee802_11.mac([0x23, 0x23, 0x23, 0x23, 0x23, 0x23], [0x42, 0x42, 0x42, 0x42, 0x42, 0x42], [0xff, 0xff, 0xff, 0xff, 0xff, 0xff])
        self.ieee802_11_chunks_to_symbols_xx_0 = ieee802_11.chunks_to_symbols()
        self.ieee802_11_chunks_to_symbols_xx_0.set_min_output_buffer((max_symbols * 48 * 8))
        # Create the options list
        self._freq_options = [2412000000.0, 2417000000.0, 2422000000.0, 2427000000.0, 2432000000.0, 2437000000.0, 2442000000.0, 2447000000.0, 2452000000.0, 2457000000.0, 2462000000.0, 2467000000.0, 2472000000.0, 2484000000.0, 5170000000.0, 5180000000.0, 5190000000.0, 5200000000.0, 5210000000.0, 5220000000.0, 5230000000.0, 5240000000.0, 5250000000.0, 5260000000.0, 5270000000.0, 5280000000.0, 5290000000.0, 5300000000.0, 5310000000.0, 5320000000.0, 5500000000.0, 5510000000.0, 5520000000.0, 5530000000.0, 5540000000.0, 5550000000.0, 5560000000.0, 5570000000.0, 5580000000.0, 5590000000.0, 5600000000.0, 5610000000.0, 5620000000.0, 5630000000.0, 5640000000.0, 5660000000.0, 5670000000.0, 5680000000.0, 5690000000.0, 5700000000.0, 5710000000.0, 5720000000.0, 5745000000.0, 5755000000.0, 5765000000.0, 5775000000.0, 5785000000.0, 5795000000.0, 5805000000.0, 5825000000.0, 5860000000.0, 5870000000.0, 5880000000.0, 5890000000.0, 5900000000.0, 5910000000.0, 5920000000.0]
        # Create the labels list
        self._freq_labels = ['  1 | 2412.0 | 11g', '  2 | 2417.0 | 11g', '  3 | 2422.0 | 11g', '  4 | 2427.0 | 11g', '  5 | 2432.0 | 11g', '  6 | 2437.0 | 11g', '  7 | 2442.0 | 11g', '  8 | 2447.0 | 11g', '  9 | 2452.0 | 11g', ' 10 | 2457.0 | 11g', ' 11 | 2462.0 | 11g', ' 12 | 2467.0 | 11g', ' 13 | 2472.0 | 11g', ' 14 | 2484.0 | 11g', ' 34 | 5170.0 | 11a', ' 36 | 5180.0 | 11a', ' 38 | 5190.0 | 11a', ' 40 | 5200.0 | 11a', ' 42 | 5210.0 | 11a', ' 44 | 5220.0 | 11a', ' 46 | 5230.0 | 11a', ' 48 | 5240.0 | 11a', ' 50 | 5250.0 | 11a', ' 52 | 5260.0 | 11a', ' 54 | 5270.0 | 11a', ' 56 | 5280.0 | 11a', ' 58 | 5290.0 | 11a', ' 60 | 5300.0 | 11a', ' 62 | 5310.0 | 11a', ' 64 | 5320.0 | 11a', '100 | 5500.0 | 11a', '102 | 5510.0 | 11a', '104 | 5520.0 | 11a', '106 | 5530.0 | 11a', '108 | 5540.0 | 11a', '110 | 5550.0 | 11a', '112 | 5560.0 | 11a', '114 | 5570.0 | 11a', '116 | 5580.0 | 11a', '118 | 5590.0 | 11a', '120 | 5600.0 | 11a', '122 | 5610.0 | 11a', '124 | 5620.0 | 11a', '126 | 5630.0 | 11a', '128 | 5640.0 | 11a', '132 | 5660.0 | 11a', '134 | 5670.0 | 11a', '136 | 5680.0 | 11a', '138 | 5690.0 | 11a', '140 | 5700.0 | 11a', '142 | 5710.0 | 11a', '144 | 5720.0 | 11a', '149 | 5745.0 | 11a (SRD)', '151 | 5755.0 | 11a (SRD)', '153 | 5765.0 | 11a (SRD)', '155 | 5775.0 | 11a (SRD)', '157 | 5785.0 | 11a (SRD)', '159 | 5795.0 | 11a (SRD)', '161 | 5805.0 | 11a (SRD)', '165 | 5825.0 | 11a (SRD)', '172 | 5860.0 | 11p', '174 | 5870.0 | 11p', '176 | 5880.0 | 11p', '178 | 5890.0 | 11p', '180 | 5900.0 | 11p', '182 | 5910.0 | 11p', '184 | 5920.0 | 11p']
        # Create the combo box
        self._freq_tool_bar = Qt.QToolBar(self)
        self._freq_tool_bar.addWidget(Qt.QLabel("'freq'" + ": "))
        self._freq_combo_box = Qt.QComboBox()
        self._freq_tool_bar.addWidget(self._freq_combo_box)
        for _label in self._freq_labels: self._freq_combo_box.addItem(_label)
        self._freq_callback = lambda i: Qt.QMetaObject.invokeMethod(self._freq_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._freq_options.index(i)))
        self._freq_callback(self.freq)
        self._freq_combo_box.currentIndexChanged.connect(
            lambda i: self.set_freq(self._freq_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._freq_tool_bar)
        self.foo_packet_pad2_0 = foo.packet_pad2(False, False, 0.001, 500, 0)
        self.foo_packet_pad2_0.set_min_output_buffer((out_buf_size * 10))
        self.fft_vxx_0_0 = fft.fft_vcc(64, False, tuple([1/52**.5] * 64), True, 1)
        self.fft_vxx_0_0.set_min_output_buffer((max_symbols * 48 * 8 * 10))
        self.digital_packet_headergenerator_bb_0 = digital.packet_headergenerator_bb(header_formatter.formatter(), "packet_len")
        self.digital_ofdm_cyclic_prefixer_0_0 = digital.ofdm_cyclic_prefixer(
            64,
            64 + 16,
            2,
            "packet_len")
        self.digital_ofdm_cyclic_prefixer_0_0.set_min_output_buffer((max_symbols * 48 * 8 * 10))
        self.digital_ofdm_carrier_allocator_cvc_0_0_0 = digital.ofdm_carrier_allocator_cvc( 64, (list(range(-26, -21)) + list(range(-20, -7)) + list(range(-6, 0)) + list(range(1, 7)) + list(range(8, 21)) +list( range(22, 27)),), ((-21, -7, 7, 21), ), ((1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1), (-1, -1, -1, 1)), ((0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, (1.4719601443879746+1.4719601443879746j), 0.0, 0.0, 0.0, (-1.4719601443879746-1.4719601443879746j), 0.0, 0.0, 0.0, (1.4719601443879746+1.4719601443879746j), 0.0, 0.0, 0.0, (-1.4719601443879746-1.4719601443879746j), 0.0, 0.0, 0.0, (-1.4719601443879746-1.4719601443879746j), 0.0, 0.0, 0.0, (1.4719601443879746+1.4719601443879746j), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, (-1.4719601443879746-1.4719601443879746j), 0.0, 0.0, 0.0, (-1.4719601443879746-1.4719601443879746j), 0.0, 0.0, 0.0, (1.4719601443879746+1.4719601443879746j), 0.0, 0.0, 0.0, (1.4719601443879746+1.4719601443879746j), 0.0, 0.0, 0.0, (1.4719601443879746+1.4719601443879746j), 0.0, 0.0, 0.0, (1.4719601443879746+1.4719601443879746j), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, (1.4719601443879746+1.4719601443879746j), 0.0, 0.0, 0.0, (-1.4719601443879746-1.4719601443879746j), 0.0, 0.0, 0.0, (1.4719601443879746+1.4719601443879746j), 0.0, 0.0, 0.0, (-1.4719601443879746-1.4719601443879746j), 0.0, 0.0, 0.0, (-1.4719601443879746-1.4719601443879746j), 0.0, 0.0, 0.0, (1.4719601443879746+1.4719601443879746j), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, (-1.4719601443879746-1.4719601443879746j), 0.0, 0.0, 0.0, (-1.4719601443879746-1.4719601443879746j), 0.0, 0.0, 0.0, (1.4719601443879746+1.4719601443879746j), 0.0, 0.0, 0.0, (1.4719601443879746+1.4719601443879746j), 0.0, 0.0, 0.0, (1.4719601443879746+1.4719601443879746j), 0.0, 0.0, 0.0, (1.4719601443879746+1.4719601443879746j), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), (0, 0j, 0, 0j, 0, 0j, -1, 1j, -1, 1j, -1, 1j, -1, -1j, 1, 1j, 1, -1j, -1, 1j, 1, 1j, 1, 1j, 1, 1j, -1, (-0-1j), 1, -1j, -1, 1j, 0, -1j, 1, (-0-1j), 1, -1j, 1, 1j, -1, -1j, 1, (-0-1j), -1, 1j, 1, 1j, 1, 1j, 1, 1j, -1, -1j, 1, 1j, 1, -1j, -1, 0j, 0, 0j, 0, 0j), (0, 0, 0, 0, 0, 0, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 0, 1, -1, -1, 1, 1, -1, 1, -1, 1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, 1, 1, 1, 0, 0, 0, 0, 0)), "packet_len", True)
        self.digital_ofdm_carrier_allocator_cvc_0_0_0.set_min_output_buffer((max_symbols * 48 * 8))
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc([-1, 1], 1)
        self.digital_chunks_to_symbols_xx_0.set_min_output_buffer((max_symbols * 48 * 8 * 2))
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=1,
            frequency_offset=(epsilon * 5.89e9 / 10e6),
            epsilon=1.0,
            taps=[1.0],
            noise_seed=0,
            block_tags=False)
        # Create the options list
        self._chan_est_options = [0, 1, 2, 3]
        # Create the labels list
        self._chan_est_labels = ['LS', 'LMS', 'Linear Comb', 'STA']
        # Create the combo box
        # Create the radio buttons
        self._chan_est_group_box = Qt.QGroupBox("'chan_est'" + ": ")
        self._chan_est_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._chan_est_button_group = variable_chooser_button_group()
        self._chan_est_group_box.setLayout(self._chan_est_box)
        for i, _label in enumerate(self._chan_est_labels):
            radio_button = Qt.QRadioButton(_label)
            self._chan_est_box.addWidget(radio_button)
            self._chan_est_button_group.addButton(radio_button, i)
        self._chan_est_callback = lambda i: Qt.QMetaObject.invokeMethod(self._chan_est_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._chan_est_options.index(i)))
        self._chan_est_callback(self.chan_est)
        self._chan_est_button_group.buttonClicked[int].connect(
            lambda i: self.set_chan_est(self._chan_est_options[i]))
        self.top_layout.addWidget(self._chan_est_group_box)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, "packet_len", 1)
        self.blocks_tagged_stream_mux_0.set_min_output_buffer((max_symbols * 48 * 8))
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc((10**(snr/10.0))**.5, 1)
        self.blocks_moving_average_xx_1 = blocks.moving_average_ff((window_size  + 16), 1, 4000, 1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_cc(window_size, 1, 4000, 1)
        self.blocks_message_strobe_0_0 = blocks.message_strobe(pmt.intern("".join("x" for i in range(pdu_length))), interval)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, 16)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, sync_length)
        self.blocks_conjugate_cc_0 = blocks.conjugate_cc()
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0_0, 'strobe'), (self.ieee802_11_mac_0_0, 'app in'))
        self.msg_connect((self.ieee802_11_mac_0_0, 'phy out'), (self.ieee802_11_mapper_0, 'in'))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_1, 0))
        self.connect((self.blocks_conjugate_cc_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_delay_0, 0), (self.sync_long, 1))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_conjugate_cc_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.sync_short, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self.sync_short, 2))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.sync_short, 1))
        self.connect((self.blocks_moving_average_xx_1, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_ofdm_carrier_allocator_cvc_0_0_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.digital_ofdm_cyclic_prefixer_0_0, 0), (self.foo_packet_pad2_0, 0))
        self.connect((self.digital_packet_headergenerator_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.digital_ofdm_cyclic_prefixer_0_0, 0))
        self.connect((self.foo_packet_pad2_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.ieee802_11_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.ieee802_11_mapper_0, 0), (self.digital_packet_headergenerator_bb_0, 0))
        self.connect((self.ieee802_11_mapper_0, 0), (self.ieee802_11_chunks_to_symbols_xx_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.sync_long, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.sync_long, 0), (self.wireless_dump_wifi_dump_0, 0))
        self.connect((self.sync_short, 0), (self.blocks_delay_0, 0))
        self.connect((self.sync_short, 0), (self.sync_long, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "wifi_loopback_phy_dump")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sensitivity(self):
        return self.sensitivity

    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity

    def get_window_size(self):
        return self.window_size

    def set_window_size(self, window_size):
        self.window_size = window_size
        self.blocks_moving_average_xx_0.set_length_and_scale(self.window_size, 1)
        self.blocks_moving_average_xx_1.set_length_and_scale((self.window_size  + 16), 1)

    def get_sync_length(self):
        return self.sync_length

    def set_sync_length(self, sync_length):
        self.sync_length = sync_length
        self.blocks_delay_0.set_dly(int(self.sync_length))

    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        self.blocks_multiply_const_xx_0.set_k((10**(self.snr/10.0))**.5)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self._samp_rate_callback(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_pdu_length(self):
        return self.pdu_length

    def set_pdu_length(self, pdu_length):
        self.pdu_length = pdu_length
        self.blocks_message_strobe_0_0.set_msg(pmt.intern("".join("x" for i in range(self.pdu_length))))
        self.wireless_dump_wifi_dump_0.set_pdu_len(self.pdu_length)

    def get_out_buf_size(self):
        return self.out_buf_size

    def set_out_buf_size(self, out_buf_size):
        self.out_buf_size = out_buf_size

    def get_max_symbols(self):
        return self.max_symbols

    def set_max_symbols(self, max_symbols):
        self.max_symbols = max_symbols

    def get_interval(self):
        return self.interval

    def set_interval(self, interval):
        self.interval = interval
        self.blocks_message_strobe_0_0.set_period(self.interval)

    def get_header_formatter(self):
        return self.header_formatter

    def set_header_formatter(self, header_formatter):
        self.header_formatter = header_formatter

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_callback(self.freq)

    def get_epsilon(self):
        return self.epsilon

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon
        self.channels_channel_model_0.set_frequency_offset((self.epsilon * 5.89e9 / 10e6))
        self.pfb_arb_resampler_xxx_0.set_rate((1+self.epsilon))

    def get_encoding(self):
        return self.encoding

    def set_encoding(self, encoding):
        self.encoding = encoding
        self._encoding_callback(self.encoding)
        self.ieee802_11_mapper_0.set_encoding(self.encoding)

    def get_chan_est(self):
        return self.chan_est

    def set_chan_est(self, chan_est):
        self.chan_est = chan_est
        self._chan_est_callback(self.chan_est)

    def get_Debug(self):
        return self.Debug

    def set_Debug(self, Debug):
        self.Debug = Debug
        self._Debug_callback(self.Debug)
        self.wireless_dump_wifi_dump_0.set_debug(self.Debug)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--sensitivity", dest="sensitivity", type=eng_float, default=eng_notation.num_to_str(float(0.56)),
        help="Set sensitivity [default=%(default)r]")
    return parser


def main(top_block_cls=wifi_loopback_phy_dump, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(sensitivity=options.sensitivity)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
