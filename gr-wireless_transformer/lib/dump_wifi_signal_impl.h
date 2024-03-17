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

     public:
      dump_wifi_signal_impl();
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
