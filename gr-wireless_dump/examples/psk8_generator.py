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
import pmt
from gnuradio import digital
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
from gnuradio.filter import pfb
import sip



class psk8_generator(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "psk8_generator")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 8
        self.samp_rate = samp_rate = 32000
        self.gain = gain = .5
        self.carrier_freq = carrier_freq = 2400e6
        self.QPSK = QPSK = digital.constellation_qpsk().base()
        self.QPSK.set_npwr(1.0)
        self.QAM64 = QAM64 = digital.constellation_calcdist([-1.0000 + 1.0000j,  -1.0000 + 0.7143j,  -1.0000 + 0.1429j,  -1.0000 + 0.4286j,  -1.0000 - 1.0000j,  -1.0000 - 0.7143j,  -1.0000 - 0.1429j,  -1.0000 - 0.4286j,  -0.7143 + 1.0000j,  -0.7143 + 0.7143j,  -0.7143 + 0.1429j,  -0.7143 + 0.4286j,  -0.7143 - 1.0000j,  -0.7143 - 0.7143j,  -0.7143 - 0.1429j,  -0.7143 - 0.4286j,  -0.1429 + 1.0000j,  -0.1429 + 0.7143j,  -0.1429 + 0.1429j,  -0.1429 + 0.4286j,  -0.1429 - 1.0000j,  -0.1429 - 0.7143j,  -0.1429 - 0.1429j,  -0.1429 - 0.4286j,  -0.4286 + 1.0000j,  -0.4286 + 0.7143j,  -0.4286 + 0.1429j,  -0.4286 + 0.4286j,  -0.4286 - 1.0000j,  -0.4286 - 0.7143j,  -0.4286 - 0.1429j,  -0.4286 - 0.4286j,   1.0000 + 1.0000j,   1.0000 + 0.7143j,   1.0000 + 0.1429j,   1.0000 + 0.4286j,   1.0000 - 1.0000j,   1.0000 - 0.7143j,   1.0000 - 0.1429j,   1.0000 - 0.4286j,   0.7143 + 1.0000j,   0.7143 + 0.7143j,   0.7143 + 0.1429j,   0.7143 + 0.4286j,   0.7143 - 1.0000j,   0.7143 - 0.7143j,   0.7143 - 0.1429j,   0.7143 - 0.4286j,   0.1429 + 1.0000j,   0.1429 + 0.7143j,   0.1429 + 0.1429j,   0.1429 + 0.4286j,   0.1429 - 1.0000j,   0.1429 - 0.7143j,   0.1429 - 0.1429j,   0.1429 - 0.4286j,   0.4286 + 1.0000j,   0.4286 + 0.7143j,   0.4286 + 0.1429j,   0.4286 + 0.4286j,   0.4286 - 1.0000j,   0.4286 - 0.7143j,   0.4286 - 0.1429j,   0.4286 - 0.4286j], [0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17,  18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,  36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,  54, 55, 56, 57, 58, 59, 60, 61, 62, 63],
        4, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.QAM64.set_npwr(1.0)
        self.QAM16 = QAM16 = digital.constellation_16qam().base()
        self.QAM16.set_npwr(1.0)
        self.PSK8 = PSK8 = digital.constellation_8psk().base()
        self.PSK8.set_npwr(1.0)
        self.BPSK = BPSK = digital.constellation_bpsk().base()
        self.BPSK.set_npwr(1.0)

        ##################################################
        # Blocks
        ##################################################

        self._gain_range = qtgui.Range(0.0, 1.0, 0.05, .5, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "'gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_win)
        self._carrier_freq_range = qtgui.Range(2400e6, 3800e6, 5e6, 2400e6, 200)
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
        self.uhd_usrp_sink_0.set_normalized_gain(gain, 0)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


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
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)



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
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
            sps,
            taps=firdes.root_raised_cosine(32, 32, 1.0, 0.35, 32*11*8),
            flt_size=32,
            atten=100)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=BPSK,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False,
            truncate=False)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/chunchi/Desktop/wireless_transformer/gr-wireless_dump/examples/you_are_very_on_time.txt', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.uhd_usrp_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "psk8_generator")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.pfb_arb_resampler_xxx_0.set_rate(self.sps)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink_0.set_normalized_gain(self.gain, 0)

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.uhd_usrp_sink_0.set_center_freq(self.carrier_freq, 0)

    def get_QPSK(self):
        return self.QPSK

    def set_QPSK(self, QPSK):
        self.QPSK = QPSK

    def get_QAM64(self):
        return self.QAM64

    def set_QAM64(self, QAM64):
        self.QAM64 = QAM64

    def get_QAM16(self):
        return self.QAM16

    def set_QAM16(self, QAM16):
        self.QAM16 = QAM16

    def get_PSK8(self):
        return self.PSK8

    def set_PSK8(self, PSK8):
        self.PSK8 = PSK8

    def get_BPSK(self):
        return self.BPSK

    def set_BPSK(self, BPSK):
        self.BPSK = BPSK




def main(top_block_cls=psk8_generator, options=None):

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
