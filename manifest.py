add_library("unix-ffi", "$(MPY_LIB_DIR)/unix-ffi")

require("mip-cmdline")
require("ssl")

include("lib")
module("makeweb/__init__.py")
module("makeweb/constants.py")
module("makeweb/dictdb.py")
module("makeweb/html.py")
module("makeweb/markdown.py")
module("main.py")
