/* -*- c++ -*- */
/*
 * Copyright 2024 gr-wireless_transformer author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "dump_wifi_signal_impl.h"

#include <gnuradio/fft/fft.h>
#include <gnuradio/filter/fir_filter.h>

#include <volk/volk.h>
#include <list>
#include <tuple>

namespace gr {
  namespace wireless_transformer {

    // #pragma message("set the following appropriately and remove this warning")
    using input_type = gr_complex;
    // #pragma message("set the following appropriately and remove this warning")
    using output_type = gr_complex;

    // make function
    dump_wifi_signal::sptr
    dump_wifi_signal::make(unsigned int window_size, double sensitivity, unsigned int sync_length)
    {
      return gnuradio::get_initial_sptr(
        new dump_wifi_signal_impl(window_size, sensitivity, sync_length));
    }

    /*
     * The private constructor
     */
    dump_wifi_signal_impl::dump_wifi_signal_impl(unsigned int window_size, double sensitivity, unsigned int sync_length)
      : gr::block("dump_wifi_signal",
              gr::io_signature::make(1 /* min inputs */, 1 /* max inputs */, sizeof(input_type)),
              gr::io_signature::make(1 /* min outputs */, 1 /*max outputs */, sizeof(output_type))), 
        d_fir(gr::filter::kernel::fir_filter_ccc(LONG)),
        d_log(log),
        d_debug(debug),
        d_offset(0),
        d_state(SYNC),
        SYNC_LENGTH(sync_length)
    {
      d_correlation = (gr_complex*)volk_malloc(sizeof(gr_complex) * 8192, volk_get_alignment());
    }

    /*
     * Our virtual destructor.
     */
    dump_wifi_signal_impl::~dump_wifi_signal_impl() {}

    // TODO
    void
    dump_wifi_signal_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
    // #pragma message("implement a forecast that fills in how many items on each input you need to produce noutput_items and remove this warning")
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
      /* Check if the input is in-sync 
        If is in-sync:
          ninput_itemsrequired[0] = 64;
          ninput_itemsrequired[1] = 64;
        If not:
          ninput_itemsrequired[0] = noutput_items;
          ninput_itemsrequired[1] = noutput_items;
      */
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

    const std::vector<gr_complex> sync_long_impl::LONG = {
      gr_complex(-0.0455, -1.0679), gr_complex(0.3528, -0.9865),
      gr_complex(0.8594, 0.7348),   gr_complex(0.1874, 0.2475),
      gr_complex(0.5309, -0.7784),  gr_complex(-1.0218, -0.4897),
      gr_complex(-0.3401, -0.9423), gr_complex(0.8657, -0.2298),
      gr_complex(0.4734, 0.0362),   gr_complex(0.0088, -1.0207),
      gr_complex(-1.2142, -0.4205), gr_complex(0.2172, -0.5195),
      gr_complex(0.5207, -0.1326),  gr_complex(-0.1995, 1.4259),
      gr_complex(1.0583, -0.0363),  gr_complex(0.5547, -0.5547),
      gr_complex(0.3277, 0.8728),   gr_complex(-0.5077, 0.3488),
      gr_complex(-1.1650, 0.5789),  gr_complex(0.7297, 0.8197),
      gr_complex(0.6173, 0.1253),   gr_complex(-0.5353, 0.7214),
      gr_complex(-0.5011, -0.1935), gr_complex(-0.3110, -1.3392),
      gr_complex(-1.0818, -0.1470), gr_complex(-1.1300, -0.1820),
      gr_complex(0.6663, -0.6571),  gr_complex(-0.0249, 0.4773),
      gr_complex(-0.8155, 1.0218),  gr_complex(0.8140, 0.9396),
      gr_complex(0.1090, 0.8662),   gr_complex(-1.3868, -0.0000),
      gr_complex(0.1090, -0.8662),  gr_complex(0.8140, -0.9396),
      gr_complex(-0.8155, -1.0218), gr_complex(-0.0249, -0.4773),
      gr_complex(0.6663, 0.6571),   gr_complex(-1.1300, 0.1820),
      gr_complex(-1.0818, 0.1470),  gr_complex(-0.3110, 1.3392),
      gr_complex(-0.5011, 0.1935),  gr_complex(-0.5353, -0.7214),
      gr_complex(0.6173, -0.1253),  gr_complex(0.7297, -0.8197),
      gr_complex(-1.1650, -0.5789), gr_complex(-0.5077, -0.3488),
      gr_complex(0.3277, -0.8728),  gr_complex(0.5547, 0.5547),
      gr_complex(1.0583, 0.0363),   gr_complex(-0.1995, -1.4259),
      gr_complex(0.5207, 0.1326),   gr_complex(0.2172, 0.5195),
      gr_complex(-1.2142, 0.4205),  gr_complex(0.0088, 1.0207),
      gr_complex(0.4734, -0.0362),  gr_complex(0.8657, 0.2298),
      gr_complex(-0.3401, 0.9423),  gr_complex(-1.0218, 0.4897),
      gr_complex(0.5309, 0.7784),   gr_complex(0.1874, -0.2475),
      gr_complex(0.8594, -0.7348),  gr_complex(0.3528, 0.9865),
      gr_complex(-0.0455, 1.0679),  gr_complex(1.3868, -0.0000),
    };

  } /* namespace wireless_transformer */
} /* namespace gr */


