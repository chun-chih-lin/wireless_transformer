/* -*- c++ -*- */
/*
 * Copyright 2024 gr-wireless_transformer author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_WIRELESS_TRANSFORMER_DUMP_WIFI_SIGNAL_H
#define INCLUDED_WIRELESS_TRANSFORMER_DUMP_WIFI_SIGNAL_H

#include <gnuradio/wireless_transformer/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace wireless_transformer {

    /*!
     * \brief <+description of block+>
     * \ingroup wireless_transformer
     *
     */
    class WIRELESS_TRANSFORMER_API dump_wifi_signal : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<dump_wifi_signal> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of wireless_transformer::dump_wifi_signal.
       *
       * To avoid accidental use of raw pointers, wireless_transformer::dump_wifi_signal's
       * constructor is in a private implementation
       * class. wireless_transformer::dump_wifi_signal::make is the public interface for
       * creating new instances.
       */
      static sptr make(unsigned int window_size, float sensitivity, unsigned int sync_length);
    };

  } // namespace wireless_transformer
} // namespace gr

#endif /* INCLUDED_WIRELESS_TRANSFORMER_DUMP_WIFI_SIGNAL_H */
