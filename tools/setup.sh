#!/bin/sh
#
# Setup script for MakeWeb.
#

is_submodule() {
    target_path="$1"

    # Check if path exists in .gitmodules file
    git config -f .gitmodules --get-regexp path | grep -q "$target_path\$"
}

add_submodule() {
    repo_url="$1"
    target_path="$2"

    if [ -z "$repo_url" ] || [ -z "$target_path" ]; then
        echo "Usage: add_submodule <repo_url> <target_path>"
        return 1
    fi

    if is_submodule "$target_path"; then
        echo "Submodule '$target_path' already exists"
        return 0
    fi

    git submodule add --depth 1 "$repo_url" "$target_path"
}

update_submodule() {
    target_path="$1"
    branch="$2"

    if [ -z "$target_path" ] || [ -z "$branch" ]; then
        echo "Usage: update_submodule <target_path> <branch>"
        return 1
    fi

    # Enter submodule directory
    cd "$target_path" || return 1

    # Fetch latest changes and reset to the remote branch
    git fetch origin "$branch"
    git reset --hard "origin/$branch"

    # Return to parent directory
    cd - >/dev/null || exit
}

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
    echo "$upstream_name: installed $(basename "$source_path")"
}

add_submodule "https://github.com/micropython/micropython" "upstream/micropython"
update_submodule "upstream/micropython" "master"
cd upstream/micropython || exit
git submodule update --init lib/mbedtls
git submodule update --init lib/berkeley-db-1.xx
git submodule update --init lib/micropython-lib
cd - || exit

echo ""
echo "---"

add_submodule "https://github.com/micropython/micropython-lib" "upstream/micropython-lib"
update_submodule "upstream/micropython-lib" "master"
echo ""
echo "---"

add_submodule "https://github.com/miguelgrinberg/microdot" "upstream/microdot"
update_submodule "upstream/microdot" "main"
echo ""
echo "---"

# Install libraries

echo "Installing libraries..."

echo "--- micropython/extmod"
install_library_from_upstream "micropython" "extmod/asyncio"
echo ""
echo "--- micropython-lib/python-stdlib"
install_library_from_upstream "micropython-lib" "python-stdlib/datetime/datetime.py"
install_library_from_upstream "micropython-lib" "python-stdlib/hmac/hmac.py"
install_library_from_upstream "micropython-lib" "python-stdlib/time/time.py"
install_library_from_upstream "micropython-lib" "python-stdlib/unittest/unittest"
install_library_from_upstream "micropython-lib" "python-stdlib/unittest-discover/unittest"
echo ""
echo "--- micropython-lib/unix-ffi"
install_library_from_upstream "micropython-lib" "unix-ffi/ffilib/ffilib.py"
echo ""
echo "--- microdot"
install_library_from_upstream "microdot" "src/microdot"
echo ""
