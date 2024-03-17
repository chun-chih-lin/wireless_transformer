# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT wireless_transformer_sources)
    message(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT wireless_transformer_sources)

########################################################################
# Check for pygccxml
########################################################################
gr_python_check_module_raw("pygccxml" "import pygccxml" PYGCCXML_FOUND)

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND wireless_transformer_python_files python_bindings.cc)

gr_pybind_make_oot(wireless_transformer ../../.. gr::wireless_transformer "${wireless_transformer_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(
    TARGET wireless_transformer_python
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:wireless_transformer_python>
            ${PROJECT_BINARY_DIR}/test_modules/gnuradio/wireless_transformer/)

install(
    TARGETS wireless_transformer_python
    DESTINATION ${GR_PYTHON_DIR}/gnuradio/wireless_transformer
    COMPONENT pythonapi)
