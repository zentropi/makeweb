#!/bin/sh
#
# Setup script for MakeWeb.
#

ensure_lib_dir() {
    # Create lib directory if it doesn't exist
    if [ ! -d "lib" ]; then
        mkdir -p "lib"
    fi
}

install_library_from_upstream() {
    upstream_name="$1"
    source_path="$2"

    if [ -z "$upstream_name" ] || [ -z "$source_path" ]; then
        echo "Usage: install_library_from_upstream <upstream_name> <source_path>"
        return 1
    fi

    ensure_lib_dir
    source_path="upstream/$upstream_name/$source_path"

    cp -r "$source_path" "lib/" 2>/dev/null || echo "Failed to copy $source_path"
    echo "  $(basename "$source_path")"
}

echo "Setting up MakeWeb development environment..."
echo "---"

echo "Updating submodule: upstream/micropython"
git submodule update --init upstream/micropython

cd upstream/micropython || exit
echo "Updating micropython submodule: lib/mbedtls"
git submodule update --init lib/mbedtls

echo "Updating micropython submodule: lib/berkeley-db-1.xx"
git submodule update --init lib/berkeley-db-1.xx

echo "Updating micropython submodule: lib/micropython-lib"
git submodule update --init lib/micropython-lib
cd - >/dev/null || exit

echo "Updating submodule: upstream/micropython-lib"
git submodule update --init upstream/micropython-lib

echo "Updating submodule: upstream/microdot"
git submodule update --init upstream/microdot
echo "---"

# Install libraries

echo "Installing libraries..."

echo "micropython/extmod"
install_library_from_upstream "micropython" "extmod/asyncio"
echo ""

echo "micropython-lib/python-stdlib"
install_library_from_upstream "micropython-lib" "python-stdlib/datetime/datetime.py"
install_library_from_upstream "micropython-lib" "python-stdlib/fnmatch/fnmatch.py"
install_library_from_upstream "micropython-lib" "python-stdlib/functools/functools.py"
install_library_from_upstream "micropython-lib" "python-stdlib/hmac/hmac.py"
# install_library_from_upstream "micropython-lib" "python-stdlib/os/os"
install_library_from_upstream "micropython-lib" "python-stdlib/os-path/os"
install_library_from_upstream "micropython-lib" "python-stdlib/stat/stat.py"
install_library_from_upstream "micropython-lib" "python-stdlib/time/time.py"
install_library_from_upstream "micropython-lib" "python-stdlib/unittest/unittest"
install_library_from_upstream "micropython-lib" "python-stdlib/unittest-discover/unittest"
echo ""

echo "micropython-lib/unix-ffi"
install_library_from_upstream "micropython-lib" "unix-ffi/ffilib/ffilib.py"
install_library_from_upstream "micropython-lib" "unix-ffi/os/os"
echo ""

echo "microdot"
install_library_from_upstream "microdot" "src/microdot"
echo ""

echo "Done."
