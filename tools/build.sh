#!/bin/sh
#
# Build script for MakeWeb.
#

get_make_command() {
    if command -v gmake >/dev/null 2>&1; then
        echo "gmake"
    else
        # Check if we're on FreeBSD
        if [ "$(uname)" = "FreeBSD" ]; then
            echo "ERROR: gmake is required on FreeBSD" >&2
            exit 1
        else
            # Fall back to make on other systems
            echo "make"
        fi
    fi
}

MAKE_CMD=$(get_make_command)

build_manifest() {
    dir=$1
    output_file="$dir/manifest.py"

    echo "Creating $dir manifest file..."

    # A little dance to avoid including the manifest file itself.
    rm -f "$output_file"
    find "$dir" -name "*.py" | sed "s|^$dir/||" | awk '{print "module(\"" $1 "\")"}' >"${dir}_manifest.py"
    mv "${dir}_manifest.py" "$output_file"
}

build_manifest "lib"
build_manifest "makeweb"

manifest_path="$(pwd)/manifest.py"
makeweb_binary_path=~/bin/makeweb

# Get original binary size before building (if exists)
original_size=0
if [ -f "$makeweb_binary_path" ]; then
    original_size=$(du -k "$makeweb_binary_path" | cut -f1)
fi

# Build mpy-cross
echo "Building mpy-cross..."
cd upstream/micropython/mpy-cross &&
    $MAKE_CMD || exit

# Return to project root
cd - >/dev/null || exit

# Build MakeWeb binary
echo "Building MakeWeb binary..."
cd upstream/micropython/ports/unix &&
    $MAKE_CMD FROZEN_MANIFEST="$manifest_path" CFLAGS_EXTRA="-Wno-error -g" || exit

# Return to project root
cd - >/dev/null || exit

# Copy MakeWeb binary to project root
cp upstream/micropython/ports/unix/build-standard/micropython "$makeweb_binary_path" || exit

# Compare and display size difference
new_size=$(du -k "$makeweb_binary_path" | cut -f1)
echo "MakeWeb binary built successfully at $makeweb_binary_path"
if [ $original_size -eq 0 ]; then
    echo "Binary size: $new_size KB (new file)"
else
    size_diff=$((new_size - original_size))
    if [ $size_diff -gt 0 ]; then
        echo "Binary size: $new_size KB (increased by $size_diff KB)"
    elif [ $size_diff -lt 0 ]; then
        echo "Binary size: $new_size KB (decreased by $((-size_diff)) KB)"
    else
        echo "Binary size: $new_size KB (unchanged)"
    fi
fi
