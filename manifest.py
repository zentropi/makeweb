add_library("unix-ffi", "$(MPY_LIB_DIR)/unix-ffi")

require("mip-cmdline")
require("ssl")

include("lib")
include("makeweb")
module("main.py")
