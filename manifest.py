add_library("unix-ffi", "$(MPY_LIB_DIR)/unix-ffi")

require("mip-cmdline")
require("ssl")

include("lib")
module("makeweb/__init__.py")
module("makeweb/dictdb.py")
module("main.py")
