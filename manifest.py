add_library("unix-ffi", "$(MPY_LIB_DIR)/unix-ffi", prepend=True)

require("mip-cmdline")
require("ssl")

include("lib")
module("makeweb/__init__.py")
module("makeweb/app.py")
module("makeweb/constants.py")
module("makeweb/dictdb.py")
module("makeweb/html.py")
module("makeweb/markdown.py")
module("makeweb/sparkline.py")
module("main.py")
