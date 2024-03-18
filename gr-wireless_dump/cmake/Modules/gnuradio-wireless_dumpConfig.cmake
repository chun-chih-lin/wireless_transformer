find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_WIRELESS_DUMP gnuradio-wireless_dump)

FIND_PATH(
    GR_WIRELESS_DUMP_INCLUDE_DIRS
    NAMES gnuradio/wireless_dump/api.h
    HINTS $ENV{WIRELESS_DUMP_DIR}/include
        ${PC_WIRELESS_DUMP_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_WIRELESS_DUMP_LIBRARIES
    NAMES gnuradio-wireless_dump
    HINTS $ENV{WIRELESS_DUMP_DIR}/lib
        ${PC_WIRELESS_DUMP_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-wireless_dumpTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_WIRELESS_DUMP DEFAULT_MSG GR_WIRELESS_DUMP_LIBRARIES GR_WIRELESS_DUMP_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_WIRELESS_DUMP_LIBRARIES GR_WIRELESS_DUMP_INCLUDE_DIRS)
