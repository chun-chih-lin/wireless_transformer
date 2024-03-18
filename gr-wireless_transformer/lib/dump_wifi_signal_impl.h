/* -*- c++ -*- */
/*
 * Copyright 2024 gr-wireless_transformer author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_WIRELESS_TRANSFORMER_DUMP_WIFI_SIGNAL_IMPL_H
#define INCLUDED_WIRELESS_TRANSFORMER_DUMP_WIFI_SIGNAL_IMPL_H

#include <gnuradio/wireless_transformer/dump_wifi_signal.h>

namespace gr {
  namespace wireless_transformer {

    class dump_wifi_signal_impl : public dump_wifi_signal
    {
     private:
      // Nothing to declare in this block.
      enum { SYNC, COPY, RESET } d_state;         // v
      int d_count;
      int d_offset;                               // v
      int d_frame_start;
      float d_freq_offset;
      double d_freq_offset_short;

      gr_complex* d_correlation;                  // v
      list<pair<gr_complex, int>> d_cor;
      std::vector<gr::tag_t> d_tags;
      gr::filter::kernel::fir_filter_ccc d_fir;   // v

      const bool d_log;                           // v
      const bool d_debug;                         // v
      const int SYNC_LENGTH;                      // v

      static const std::vector<gr_complex> LONG;

     public:
      dump_wifi_signal_impl(unsigned int window_size, double sensitivity, unsigned int sync_length);
      ~dump_wifi_signal_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace wireless_transformer
} // namespace gr

#endif /* INCLUDED_WIRELESS_TRANSFORMER_DUMP_WIFI_SIGNAL_IMPL_H */
