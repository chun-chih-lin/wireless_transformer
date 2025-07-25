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
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import sip



class Record_Signal(gr.top_block, Qt.QWidget):

    def __init__(self):
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

        self.settings = Qt.QSettings("GNU Radio", "Record_Signal")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.tx_power = tx_power = "-10"
        self.save_prefix = save_prefix = "Dataset_EIB_3F_Hallway_0430"
        self.save_mod = save_mod = "RAND"
        self.samp_rate = samp_rate = 5e6
        self.interference = interference = 0
        self.distance = distance = 15
        self.carrier_freq = carrier_freq = 2360e6
        self.save_folder = save_folder = "/home/chunchi/Desktop/wireless_transformer/records/"
        self.save_filename = save_filename = "Non_process_" + save_prefix + "_" +  save_mod + "_TP" + tx_power + "_D" + str(distance) + "_SR" + str(int(samp_rate/1e6)) + "_CF" + str(int(carrier_freq/1e6)) + "_I" + str(interference) + ".dat"
        self.ttl_save_sample = ttl_save_sample = 20e3
        self.save_full_filename = save_full_filename = save_folder + save_prefix + "/" + save_filename
        self.sample_per_input = sample_per_input = 128
        self.gain_db = gain_db = 30
        self.gain = gain = .65

        ##################################################
        # Blocks
        ##################################################

        self._gain_db_range = qtgui.Range(0, 70, 1, 30, 200)
        self._gain_db_win = qtgui.RangeWidget(self._gain_db_range, self.set_gain_db, "'gain_db'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_db_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0.set_center_freq(carrier_freq, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_gain(gain_db, 0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            10240, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-0.25, 0.25)

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
        self._interference_range = qtgui.Range(0, 1, 1, 0, 200)
        self._interference_win = qtgui.RangeWidget(self._interference_range, self.set_interference, "Interference", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._interference_win, 2, 3, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_range = qtgui.Range(0, 1.0, 0.01, .65, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "'gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_win)
        self._distance_range = qtgui.Range(5, 15, 5, 15, 200)
        self._distance_win = qtgui.RangeWidget(self._distance_range, self.set_distance, "Distance", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._distance_win, 1, 0, 1, 3)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, (int(ttl_save_sample*sample_per_input)))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, save_full_filename, False)
        self.blocks_file_sink_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_head_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_head_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Record_Signal")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tx_power(self):
        return self.tx_power

    def set_tx_power(self, tx_power):
        self.tx_power = tx_power
        self.set_save_filename("Non_process_" + self.save_prefix + "_" +  self.save_mod + "_TP" + self.tx_power + "_D" + str(self.distance) + "_SR" + str(int(self.samp_rate/1e6)) + "_CF" + str(int(self.carrier_freq/1e6)) + "_I" + str(self.interference) + ".dat")

    def get_save_prefix(self):
        return self.save_prefix

    def set_save_prefix(self, save_prefix):
        self.save_prefix = save_prefix
        self.set_save_filename("Non_process_" + self.save_prefix + "_" +  self.save_mod + "_TP" + self.tx_power + "_D" + str(self.distance) + "_SR" + str(int(self.samp_rate/1e6)) + "_CF" + str(int(self.carrier_freq/1e6)) + "_I" + str(self.interference) + ".dat")
        self.set_save_full_filename(self.save_folder + self.save_prefix + "/" + self.save_filename)

    def get_save_mod(self):
        return self.save_mod

    def set_save_mod(self, save_mod):
        self.save_mod = save_mod
        self.set_save_filename("Non_process_" + self.save_prefix + "_" +  self.save_mod + "_TP" + self.tx_power + "_D" + str(self.distance) + "_SR" + str(int(self.samp_rate/1e6)) + "_CF" + str(int(self.carrier_freq/1e6)) + "_I" + str(self.interference) + ".dat")

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_save_filename("Non_process_" + self.save_prefix + "_" +  self.save_mod + "_TP" + self.tx_power + "_D" + str(self.distance) + "_SR" + str(int(self.samp_rate/1e6)) + "_CF" + str(int(self.carrier_freq/1e6)) + "_I" + str(self.interference) + ".dat")
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_interference(self):
        return self.interference

    def set_interference(self, interference):
        self.interference = interference
        self.set_save_filename("Non_process_" + self.save_prefix + "_" +  self.save_mod + "_TP" + self.tx_power + "_D" + str(self.distance) + "_SR" + str(int(self.samp_rate/1e6)) + "_CF" + str(int(self.carrier_freq/1e6)) + "_I" + str(self.interference) + ".dat")

    def get_distance(self):
        return self.distance

    def set_distance(self, distance):
        self.distance = distance
        self.set_save_filename("Non_process_" + self.save_prefix + "_" +  self.save_mod + "_TP" + self.tx_power + "_D" + str(self.distance) + "_SR" + str(int(self.samp_rate/1e6)) + "_CF" + str(int(self.carrier_freq/1e6)) + "_I" + str(self.interference) + ".dat")

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.set_save_filename("Non_process_" + self.save_prefix + "_" +  self.save_mod + "_TP" + self.tx_power + "_D" + str(self.distance) + "_SR" + str(int(self.samp_rate/1e6)) + "_CF" + str(int(self.carrier_freq/1e6)) + "_I" + str(self.interference) + ".dat")
        self.uhd_usrp_source_0.set_center_freq(self.carrier_freq, 0)

    def get_save_folder(self):
        return self.save_folder

    def set_save_folder(self, save_folder):
        self.save_folder = save_folder
        self.set_save_full_filename(self.save_folder + self.save_prefix + "/" + self.save_filename)

    def get_save_filename(self):
        return self.save_filename

    def set_save_filename(self, save_filename):
        self.save_filename = save_filename
        self.set_save_full_filename(self.save_folder + self.save_prefix + "/" + self.save_filename)

    def get_ttl_save_sample(self):
        return self.ttl_save_sample

    def set_ttl_save_sample(self, ttl_save_sample):
        self.ttl_save_sample = ttl_save_sample
        self.blocks_head_0.set_length((int(self.ttl_save_sample*self.sample_per_input)))

    def get_save_full_filename(self):
        return self.save_full_filename

    def set_save_full_filename(self, save_full_filename):
        self.save_full_filename = save_full_filename
        self.blocks_file_sink_0.open(self.save_full_filename)

    def get_sample_per_input(self):
        return self.sample_per_input

    def set_sample_per_input(self, sample_per_input):
        self.sample_per_input = sample_per_input
        self.blocks_head_0.set_length((int(self.ttl_save_sample*self.sample_per_input)))

    def get_gain_db(self):
        return self.gain_db

    def set_gain_db(self, gain_db):
        self.gain_db = gain_db
        self.uhd_usrp_source_0.set_gain(self.gain_db, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain




def main(top_block_cls=Record_Signal, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

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
