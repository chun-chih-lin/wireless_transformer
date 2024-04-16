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
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
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



class am_ssb_generator(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "am_ssb_generator")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200e3
        self.input_gain = input_gain = 0.4
        self.gain_db = gain_db = 50
        self.gain = gain = .5
        self.carrier_freq = carrier_freq = 2500e6
        self.audio_source_sampling_rate = audio_source_sampling_rate = 44.1e3

        ##################################################
        # Blocks
        ##################################################

        self._input_gain_range = qtgui.Range(0, 10, 0.1, 0.4, 200)
        self._input_gain_win = qtgui.RangeWidget(self._input_gain_range, self.set_input_gain, "'input_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._input_gain_win)
        self._gain_db_range = qtgui.Range(0, 70, 10, 50, 200)
        self._gain_db_win = qtgui.RangeWidget(self._gain_db_range, self.set_gain_db, "'gain_db'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_db_win)
        self._carrier_freq_range = qtgui.Range(2400e6, 3800e6, 5e6, 2500e6, 200)
        self._carrier_freq_win = qtgui.RangeWidget(self._carrier_freq_range, self.set_carrier_freq, "'carrier_freq'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._carrier_freq_win)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(carrier_freq, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(gain_db, 0)
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_ccf(
                interpolation=4,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=500,
                decimation=441,
                taps=[],
                fractional_bw=0)
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
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.hilbert_fc_0 = filter.hilbert_fc(401, window.WIN_HAMMING, 6.76)
        self._gain_range = qtgui.Range(0.0, 1.0, 0.05, .5, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "'gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_win)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/chunchi/Desktop/wireless_transformer/gr-wireless_dump/examples/Rick Astley  Never Gonna Give You Up.wav', True)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_cc(10)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(input_gain)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_ff(1)
        self.band_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                50e3,
                300,
                3000,
                100,
                window.WIN_HAMMING,
                6.76))
        self.analog_sig_source_x_0_0 = analog.sig_source_c(50e3, analog.GR_COS_WAVE, 10e3, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0_0, 1))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_multiply_xx_0_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.hilbert_fc_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.hilbert_fc_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "am_ssb_generator")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_input_gain(self):
        return self.input_gain

    def set_input_gain(self, input_gain):
        self.input_gain = input_gain
        self.blocks_multiply_const_vxx_0_0.set_k(self.input_gain)

    def get_gain_db(self):
        return self.gain_db

    def set_gain_db(self, gain_db):
        self.gain_db = gain_db
        self.uhd_usrp_sink_0.set_gain(self.gain_db, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.uhd_usrp_sink_0.set_center_freq(self.carrier_freq, 0)

    def get_audio_source_sampling_rate(self):
        return self.audio_source_sampling_rate

    def set_audio_source_sampling_rate(self, audio_source_sampling_rate):
        self.audio_source_sampling_rate = audio_source_sampling_rate




def main(top_block_cls=am_ssb_generator, options=None):

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
