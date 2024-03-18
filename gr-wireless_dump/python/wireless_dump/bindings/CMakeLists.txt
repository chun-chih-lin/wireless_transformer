# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT wireless_dump_sources)
    message(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT wireless_dump_sources)

########################################################################
# Check for pygccxml
########################################################################
gr_python_check_module_raw("pygccxml" "import pygccxml" PYGCCXML_FOUND)

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND wireless_dump_python_files python_bindings.cc)

gr_pybind_make_oot(wireless_dump ../../.. gr::wireless_dump "${wireless_dump_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(
    TARGET wireless_dump_python
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:wireless_dump_python>
            ${PROJECT_BINARY_DIR}/test_modules/gnuradio/wireless_dump/)

install(
    TARGETS wireless_dump_python
    DESTINATION ${GR_PYTHON_DIR}/gnuradio/wireless_dump
    COMPONENT pythonapi)
