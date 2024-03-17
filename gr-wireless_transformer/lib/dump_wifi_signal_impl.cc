/* -*- c++ -*- */
/*
 * Copyright 2024 gr-wireless_transformer author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "dump_wifi_signal_impl.h"

namespace gr {
  namespace wireless_transformer {

    #pragma message("set the following appropriately and remove this warning")
    using input_type = float;
    #pragma message("set the following appropriately and remove this warning")
    using output_type = float;
    dump_wifi_signal::sptr
    dump_wifi_signal::make()
    {
      return gnuradio::make_block_sptr<dump_wifi_signal_impl>(
        );
    }


    /*
     * The private constructor
     */
    dump_wifi_signal_impl::dump_wifi_signal_impl()
      : gr::block("dump_wifi_signal",
              gr::io_signature::make(1 /* min inputs */, 1 /* max inputs */, sizeof(input_type)),
              gr::io_signature::make(1 /* min outputs */, 1 /*max outputs */, sizeof(output_type)))
    {}

    /*
     * Our virtual destructor.
     */
    dump_wifi_signal_impl::~dump_wifi_signal_impl()
    {
    }

    void
    dump_wifi_signal_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
    #pragma message("implement a forecast that fills in how many items on each input you need to produce noutput_items and remove this warning")
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
    }

    int
    dump_wifi_signal_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      auto in = static_cast<const input_type*>(input_items[0]);
      auto out = static_cast<output_type*>(output_items[0]);

      #pragma message("Implement the signal processing in your block and remove this warning")
      // Do <+signal processing+>
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (noutput_items);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace wireless_transformer */
} /* namespace gr */
